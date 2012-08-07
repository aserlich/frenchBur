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
	File removes headers, footers, and alphabetization from index file
	Currently only tested for 2011
	"""
	import codecs
	locs = getPN(fileName)[1] 	#call getpage numebers to remove these from file
	#print(locs)
	fh = open(fileName)
	fh.seek(0)
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
	return xmod

def cleanLevels(xmod):
	"""
	This function determines whether or not an index entry is on one or two lines and parses the index entry from the page number 
	It then calls the function split level to extract more information about the level
	"""
	allLines =[]
	storage = []
	ac = regex.compile(r'\.*([1-9][0-9]{2}|[4-9][0-9])\n', flag=regex.UNICODE) #the or has to get around G20 which is in a title
	ac2 = regex.compile(r'\.*([1-9][0-9]{2}|[4-9][0-9])', flag=regex.UNICODE)
	keys = ['pageNum','fullName', 'org', 'com']
	for i in range(0, len(xmod)):
		#print(xmod[i])
		D= {key: None for key in keys}
		#or dict.fromkeys(keys, None)
		m = regex.search(ac, xmod[i])
		#print(xmod[i], i)
		if m!=None: #if there is a page number
			if i not in allLines: #and the thing hasn't been evluated before
				fe1 = xmod[i].strip()
				D['pageNum'] = m.group(1).strip()
				allLines.append(i)
				D['fullName'] = regex.split(ac2, fe1)[0]
				storage.append(D)
		elif m == None: #if there is no page number - page number is on next line
			if i not in allLines:
				fe2 = ' '.join([xmod[i].strip(), xmod[i+1].strip()])
				s1 = regex.search(ac, xmod[i+1])
				D['pageNum'] = s1.group(1).strip()
				allLines.append(i)
				allLines.append(i+1)
				D['fullName'] = regex.split(ac2, fe2)[0]
				storage.append(D)
				#if xmod[i] =='Secrétariat général de la présidence française du G20 et du G8':
					#print(xmod[i], 'is the problem')
		print(D['fullName'])
		print(i)
	splitLevel(storage)
	return([storage, allLines])

def splitLevel(recs):
	"""
	This function extracts information about the committee and ministry associated with an entry and adds it to the dictionary
	Currently called from cleanLevels()
	"""
	mnstry = regex.compile(r"\(((([\p{Lu}]{0,3}|[\p{Ll}]{1}])[\p{Ll}]{0,8}\..*)|PM|CE)\)", flag=regex.UNICODE)
	cmte = regex.compile(r"\(+?(([\p{Lu}]{3})(?!\.).*?)\)+?", flag=regex.UNICODE) #still doesn't capture typo of ECO.
	for rec in recs: 
		#print(rec['fullName'], rec['pageNum'], sep =', ')
		#this also serves as a test for errors and standardizes erros
		ms = regex.findall(mnstry, rec['fullName'])[0][0].replace(' ','').capitalize()
		rec['org'] = ms
		cm = regex.search(cmte, rec['fullName'])
		if cm != None:
			#print(cm.group(1))
			rec['nameOnly'] = regex.split(cmte, rec['fullName'])[0]
			rec['com'] = cm.group(1)
		else: 
			rec['nameOnly'] = 	regex.split(mnstry, rec['fullName'])[0]

###Code uses to call the functions and export it

xmod = getLevels('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentralesV1.1.txt')
recs = cleanLevels(xmod)
set(recs[1]) - set(range(0,1100))#check for the missing lines

keys = ['pageNum','fullName', 'org', 'com']
res = pd.DataFrame(columns=keys)
for q in range(0, len(recs[0])):
	row = pd.DataFrame((recs[0][q]), index = [q])
	res = res.append(row, ignore_index=True)

res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBurOrgs20120806V2.csv')
		

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