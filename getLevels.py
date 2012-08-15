#!/usr/bin/env python
# encoding: utf-8
"""
getLevels.py
Created by Aaron Erlich on 2012-08-03.
Tested on 2011 files
"""

import pandas as pd
import regex
import scipy
import numpy

def getLevels(fileName):
	"""
	File removes headers, footers, and alphabetization from index file, and the calls clean levels
	to turn a dictionary file of index entries.
	Currently only tested for 2011
	"""
	#import codecs
	locs = [linenums['endLoc'] for linenums in getPN(fileName)] #call getpage numebers to remove these from file
	fh = open(fileName)
	x = fh.readlines()
	fh.close()
	for i in range(0, len(x)):
		#print(x[i])
		if len(x[i].strip()) == 1 or 'index des administrations centrales' in x[i].strip().lower():
			locs.append(i) #onl evaluate if not a letter or a footer/header
	xmod = []
	for i in range(0, len(x)):
		if i not in locs:
			xmod.extend([x[i]])
	output = cleanLevels(xmod)
	return output

def cleanLevels(xmod):
	"""
	Determines whether or not an index entry is on one or two lines and parses the index entry from the page number. 
	It then calls the function split level to extract more information about the index entry -- info in the parentheses .
	"""
	evalLines =[]
	indEntries = []
	ac = regex.compile(r'\.*([1-9][0-9]{2}|[4-9][0-9])\n', flag=regex.UNICODE) #the or has to get around G20 which is in a title
	ac2 = regex.compile(r'\.*([1-9][0-9]{2}|[4-9][0-9])', flag=regex.UNICODE)
	keys = ['pageNum','fullName', 'org', 'com']
	for i in range(0, len(xmod)):
		#print(xmod[i])
		D= {key: None for key in keys}
		#or dict.fromkeys(keys, None)
		m = regex.search(ac, xmod[i])
		#print(xmod[i], i)
		if m != None: #if there is a page number THIS SHOULD BE RECURSIVE
			if i not in evalLines: #and the thing hasn't been evluated before
				fe1 = xmod[i].strip()
				D['pageNum'] = int(m.group(1).strip())
				evalLines.append(i)
				D['fullName'] = regex.split(ac2, fe1)[0]
				indEntries.append(D)
		elif m == None: #if there is no page number - page number may be on next line
			if i not in evalLines:
				fe2 = " ".join([xmod[i].strip(), xmod[i+1].strip()]) #join two lines together
				s1 = regex.search(ac, xmod[i+1]) #look for the page number in the scond line
				if s1 != None: #if its on the second line
					D['pageNum'] = int(s1.group(1).strip()) 
					evalLines.append(i)
					evalLines.append(i+1)
					D['fullName'] = regex.split(ac2, fe2)[0]
					indEntries.append(D)
				#if xmod[i] =='Secrétariat général de la présidence française du G20 et du G8':
					#print(xmod[i], 'is the problem')
				elif s1 == None:
					if i not in evalLines:
						fe3 = " ".join([fe2, xmod[i+2]])
						s2 = regex.search(ac, xmod[i+2])
						D['pageNum'] = int(s2.group(1).strip())
						evalLines.append(i+2)
						D['fullName'] = regex.split(ac2, fe3)[0]
						indEntries.append(D)
		print(D['fullName'])
		print(i)
	splitLevel(indEntries)
	index = {}
	index['indEntries'] = indEntries
	index['evalLines'] = evalLines
	return(index) # current for testing

def splitLevel(recs):
	"""
	This function extracts information about the committee and ministry associated with an entry and adds it to the dictionary
	Currently called from cleanLevels().
	"""
	mnstry = regex.compile(r"\(((([\p{Lu}]{0,3}|[\p{Ll}]{1}])[\p{Ll}]{0,8}\..*)|PM|CE)\)", flag=regex.UNICODE)
	cmte = regex.compile(r"\(+?(([\p{Lu}]{3})(?!\.).*?)\)+?", flag=regex.UNICODE) #still doesn't capture typo of ECO.
	for rec in recs: 
		#print(rec['fullName'], rec['pageNum'], sep =', ')
		#this also serves as a test for errors and standardizes erros
		ms = regex.findall(mnstry, rec['fullName'])[0][0].replace(' ','').capitalize()
		rec['org'] = ms
		cm = regex.search(cmte, rec['fullName'])
		# if cm != None:
		# 	#print(cm.group(1))
		# 	rec['nameOnly'] = regex.split(cmte, rec['fullName'])[0]
		# 	rec['com'] = cm.group(1)
		#else: 
		rec['nameOnly'] = 	(regex.split(mnstry, rec['fullName'])[0]).strip()

###Code uses to call the functions and export it

xmod = getLevels('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentralesV1.3.txt')
set(recs[1]) - set(range(0,1100))#check for the missing lines

keys = ['pageNum','fullName', 'nameOnly', 'org', 'com']
res = pd.DataFrame(columns=keys)
for q in range(0, len(xmod['indEntries'])):
	row = pd.DataFrame(xmod['indEntries'][q], index = [q])
	res = res.append(row, ignore_index=True)

res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBurOrgs20120806V2.2.csv')


def getLevelsTOC(fileName):
	"""
	More directly parses an index file by collapsing it on one line an then parsing it. 
	It omits the necessity to recursively grab lines to check for the end of the entry
	This file is designed for two levels,
	where a symbol separates the areas the belong to chunk 1
	Could be more generic by passing regular expressions in as *args for an arbitrary number of hierachical levels n
	and splitting on n+1 reu
	"""
	import functools
	fh = open(fileName)
	x = fh.readlines()
	fh.close()
	lev1 =[]
	lev2=[]
	oneLine = functools.reduce(lambda x,y: x +" " + y, [line[:-1] for line in x]) #collapse as one line this is a problem if there is no new line at the end
	minsLev = oneLine.split("►") #split all of the highest levels
	#print(minsLev)
	num = regex.compile(r'([1-9][0-9]{1,2})\s*', regex.UNICODE | regex.VERSION1) #this is just ot return the match of an number
	title = regex.compile(r'([[\p{Ll}\p{Lu}\s\'\-\(\)]--[\.]]+).*', regex.UNICODE | regex.VERSION1) #this is to return the title
	getrec = regex.compile(r'([[\D]--[0-9]]+[1-9][0-9]{1,2}\s)', regex.UNICODE | regex.VERSION1) #this is to splot both the line and the title together
	for i, stuff in enumerate(minsLev): #loop thourgh all the level 1 splits
		allrecs =regex.split(getrec, stuff)
		allrecs = filter(len, allrecs)
		print(stuff)
		#print(list(allrecs))
		#input("")
		for j, entries in enumerate(allrecs): #loop through all the level to nslits
			L = {}
			#print(entries)
			if len(entries) > 3: #hacky, but omit form feed things
				#print(entries)
				if j == 0:
					L['pageNum'] = int(regex.search(num, entries).group(1).strip())
					L['org'] = regex.search(title, entries).group(1).strip()
					lev1.append(L)
				else:
					L['pageNum'] = int(regex.search(num, entries).group(1).strip())
					L['org'] = regex.search(title, entries).group(1).strip()
					L['lev1Org'] = lev1[-1]['org']
					lev2.append(L)
			else:
				print("Look at this ENTRY", entries)
	levs = {}
	levs['lev1'] = lev1
	levs['lev2'] = lev2
	return(levs)


			
#keys = ['pageNum','org', 'Lev1Org']
res = pd.DataFrame(columns=None)
for q in range(0, len(test['lev2'])):
	row = pd.DataFrame((test['lev2'][q]), index = [q])
	res = res.append(row, ignore_index=True)
	
	
res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBurLev2Orgs20120813V1.0.csv')



#current errors
#Agro-Sup Dijon not found
#Centre INFFO not found
#Les Ateliers - ENSCI not found
# Fonds CMU
# FranceAgriMer
# VetAgro Sup
# Agrocampus Ouest
# EN3S
#issue when part of ECO is captialized and cant make regex work
#record 736??? why doesn't parse properly