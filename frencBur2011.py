#!/usr/bin/env python
# encoding: utf-8
"""
FrenchBur2011.py

Created by Aaron Erlich on 2012-08-01.
"""
import sys
import os
import regex
import pandas as pd
import numpy
import scipy

# 1) create a two dimensial array where each name gets an entry
# 2) go through the lines until I find a title
# 3) if there is text after the title, then that's the name but run checks
#4 4) if there is no text, take the next line and evaluate as the name -- put it in the db
	#if it is "N...", then make it an NA
# 5) After name is entered, evaluate following lines with regular expressions for all of the following potential info
#		1)email
#		2)tel
#		3)fax		
#		4)address
#		5) keep track of how many lines down this goes
# 6) The next line will be a title of a bureacratic level associated with the next name
#	Which needs to to stored to put into the next persons entry

#os.chdir('/Volumes/Optibay-1TB/FrenchBur/2011/output')
def firstPass(fileName):
	""""
	takes whole file and finds all locations where there is bureaucratic rank info
	"""
	fh = open(fileName)
	fh.seek(0)
	x = fh.readlines()
	allLines = [] #to store all lines in file analyzed and take advantage of nested scoping in python
	locs1 = [] #store locations of ranks to analze
	for i in range(0, len(x)):
		m = regex.search(r'•\s*(.*)\s*:\s*', x[i])
		if m != None:
			locs1.append(i)
			print(m.group(1))
	allLines = list(locs1)
	#part2 g over the file again
	locs2 = []
	garbage = []	
	for i in range(0, len(x)):
		dot = x[i].find('•')
		colon1 = x[i].find(':')
		if dot == 0 and colon1 == -1:
			colon2 = x[i+1].find(':')
			if colon2 >= 0:
				allLines.extend([x[i], x[i+1]])
				locs2.append(i+1)
				print(x[i].strip())
				print(x[i+1].strip())
			elif colon2 == -1:
				garbage.append([i,''.join([x[i].strip(), x[i+1].strip()])])
				print(''.join([x[i].strip(), x[i+1].strip()]), "IS A DAM ERROR")
			#input("Press Enter to continue...")
	print("PRELIMINARY PASSES DONE ON TO BUILDING THE DATABASE...")
	output = getNames(allLines, locs1, locs2, x)
	return(output)

def emtefa(text, D, nextRow):
	'''
	takes text, given text and a dictionary, and checks whether the text has a fax, email or phone number
	it then parses out the email fax and phone and adds it to the dict
	if the level = 0, then it assumes the name is present in the text and calls check name do pull out the name
	Currently there is no level passed but the level is set to zero
	'''
	levels = 0 #distance from original title
	#needs to bu called recursively until no other material about thee individual is available
	email = regex.compile(r'([a-zA-Z0-9+.-]+@[a-z0-9.-]+\.(fr|com|eu))', flag=regex.UNICODE)
	tel = regex.compile(r'Tél\.\s*:\s*\+*((?:[0-9]\s?){10,14})', flag=regex.UNICODE)
	fax = regex.compile(r'Fax\.\s*:\s*((?:\+*[0-9]\s?){10,14})', flag=regex.UNICODE)
	ecount = 0 
	tcount = 0
	fcount = 0
	em = regex.search(email, text)
	if  em != None:
		D['email'] = em.group(1).strip()
		#print(D['email'])
		ecount = 1
	te = regex.search(tel, text)
	if te != None:
		D['tel'] = te.group(1).strip()
		tcount = 1
	fa = regex.search(fax,  text)	
	if fa != None:
		D['fax'] = fa.group(1).strip()
		fcount = 1
	if levels == 0: #only when we are at the same level as the title
		if ecount == 1:
			nm = regex.split(email, text)
			D = checkName(nm[0].strip(), D, nextRow)
		elif tcount	== 1:
			nm = regex.split(tel, text)
			checkName(nm[0].strip(), D, nextRow)
		elif fcount	== 1:
			nm = regex.split(tel, text)
			checkName(nm[0].strip(), D, nextRow)
		else:
			checkName(text, D, nextRow)
		#print(D['name'])
	#return(D)

def checkName(nameText, D, nextRow):    # check whether material is a ph
	"""
	File runs check to make sure only a name is extracted 
	#There can be a comma with a title
	#there can be a title without a comma
	#there can be just a comma -- in which case the title is on the next line
	#if the number of words is two, assume it is a name
	#if the number of words is three or 4 and the second two are uppercase assume it is name
	"""
	nameText = nameText.strip()
	if regex.search(r',', nameText,  flag=regex.UNICODE):
		nt = nameText.split(',', 1)
		D['name'] = nt[0].strip()
		if len(nt[1].strip()) > 0:
			D['title'] = nt[1].strip()
		elif len(nt[1].strip()) == 0:
			print("comma is on end of line and title is on next. Title is:", nextRow.strip()) #this should be when there is a comma but the title is on the next line?
			D['title'] = nextRow.strip()
			input("Press Enter to continue...")
	elif len(nameText.split(" ")) == 2 or nameText == "N..." :
		D['name'] = nameText
	elif nameText == "n...":
		D['name'] = "N..."
	elif len(nameText.split(" ")) <2 and nameText != "N..." and nameText != "n...": 
		D['name'] = nameText
		D['nameFlag'] = 3
		print("is this a name text of length 1:", nameText)
		input("Press Enter to continue...")
	elif len(nameText.split(" ")) > 2:
		#find the border between the name and the non-name
		f = regex.findall(r'([\p{Lu}]{2,20}\-?\'?[\p{Lu}]{0,20})', nameText, flag=regex.UNICODE)
		if not f:
			#print(nameText, "is problematic because most likely no capital distinguished the name from the title")
			D['name'] = nameText
			D['nameFlag'] = 1
		else:
			index = nameText.find(f[-1])
			end = index +len(f[-1]) + 1
			D['name'] = nameText[0:end]
			if len(nameText[end:len(nameText)]) > 0 :
				D['title'] = nameText[end:len(nameText)]
			if len(nameText[0:end].split(" ")) > 5: #this could be better if needed length 6 is arbitrary
				D['nameFlag'] = 2
				#print(nameText, ":it is strangely long. Flag 2 added")
				#input("Press Enter to continue...")
	else:
		print("This is problematic with an undiagnosed problem", nameText)
		input("Press Enter to continue...")
	#return(D)

def getNames(allLines, locs1, locs2, x):
	"""
	Calls appropriate helper functions to accurately parse name infromation
	"""		
	locs = locs1 + locs2
	locs = sorted(locs)
	storage = []	
	keys = ['loc','name', 'nameFlag', 'rank','email','tel','fax', 'title']
	for i in locs:
		D= {key: None for key in keys}
		m = None
		D['loc'] = i
		if i in locs1:
			m = regex.split(r'•\s*(.*?):\s*',x[i]) #split line with rank
			D['rank'] = m[1].strip()
		elif i in locs2:
			m = regex.split(r'•\s*(.*?):\s*', ' '.join([x[i-1].strip(), x[i].strip()]), flag=regex.UNICODE) #do something
			D['rank'] = m[1].strip()
		if len(m[2].strip()) == 0: #if there is only a rank
		 	#assume name is on next line potentially with some other info
			allLines.append(x[i+1])
			emtefa(x[i+1], D, x[i+2])
		else:  #name is on the same line
			emtefa(m[2].strip(), D, x[i+1])
		storage.append(D)
	return([allLines,locs,storage])


###Get output
op = firstPass('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V1.3.txt')

keys = ['loc','name', 'nameFlag', 'rank','email','tel','fax', 'title']
res = pd.DataFrame(columns=keys)
for q in range(0, len(op[2])):
	row = pd.DataFrame((op[2][q]), index = [q])
	res = res.append(row, ignore_index=True)

res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120803V2.1.csv')
		
