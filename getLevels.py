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

#deprecated

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
	num = regex.compile(r'([1-9][0-9]{1,2})\s*', regex.UNICODE | regex.VERSION1) #this is just to return the match of a number
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


def getLevelsIndex(fileName):
	"""
	More directly parses an index file by collapsing it on one line an then parsing it. 
	It omits the necessity to recursively grab lines to check for the end of the entry
	This file is designed for two levels,
	where a symbol separates the areas the belong to chunk 1
	Could be more generic by passing regular expressions in as *args for an arbitrary number of hierachical levels n
	and splitting on n+1 reu
	"""
	import functools
	import operator
	fh = open(fileName)
	x = fh.readlines()
	fh.close()
	index =[]
	oneLine = functools.reduce(lambda x,y: x +" " + y, [line for line in x])
	#print(minsLev)
	num = regex.compile(r'([1-9][0-9]{2}|[4-9][0-9])\s*', regex.UNICODE | regex.VERSION1) #this is just to return the match of a number
	title = regex.compile(r'(^\s*.*\)).*', regex.UNICODE | regex.VERSION1) #this is to return the title
	getrec = regex.compile(r'\s*([\p{Lu}\p{Ll}\']{2}.*?(?:[1-9][0-9]{2}|[4-9][0-9])\s*)', regex.UNICODE | regex.VERSION1 | regex.DOTALL) #this is to splot both the line and the title together
	mnstry = regex.compile(r"\(((([\p{Lu}]{0,3}|[\p{Ll}]{1}])[\p{Ll}]{0,8}\..*)|PM|CE)\)", flag=regex.UNICODE)
	cmte = regex.compile(r"\(+?(([\p{Lu}]{3})(?!\.).*?)\)+?", flag=regex.UNICODE) #still doesn't capture typo of ECO.
	bo = regex.escape("SCBCM", regex.UNICODE)
	rbo = r'%s' % bo
	budgetOffice = regex.compile(rbo, regex.UNICODE)
	for match in getrec.finditer(oneLine):
		for item in match.groups():
			#print("ITEM MATCHED", item)
			try:
				entry = {}
				entry['pageNum'] = int(num.search(regex.sub("\n","",item)).groups(1)[0]) #need to use regex.sub to strib out line breaks
				entry['orgFull'] = title.search(regex.sub("\n","",item)).groups(1)[0]
			except AttributeError: #allow for exceptiosn where there isn't a page number or a title and just print it out
				print("Item", item, "is does not appear to have a page number or title, \
				but program will continue without entering into db")
				del(entry)
			try: 
				entry['org'] = 	regex.split(mnstry, entry['orgFull'])[0].strip()
				entry['ministry'] = mnstry.search(entry['orgFull']).groups(1)[0].replace(' ','').capitalize()
				index.append(entry)
				def specialCase(entry):
					if budgetOffice.search(entry['org']) !=None:
						entry['level'] = 0 
						print(entry)
						input(" ")
				specialCase(entry)
			except NameError:
				pass
	index = sorted(index, key=operator.itemgetter('pageNum'))
	return(index)

test = getLevelsIndex('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentralesV1.3.txt')

index = pd.DataFrame(columns=None)
for q in range(len(test)):
	row = pd.DataFrame((test[q]), index = [q])
	index = index.append(row, ignore_index=True)

	
index.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBurOrgs20120806V3.0.csv')

			
#keys = ['pageNum','org', 'Lev1Org']
res = pd.DataFrame(columns=None)
for q in range(0, len('lev2')):
	row = pd.DataFrame((lev2[q]), index = [q])
	print(row)
	res = res.append(row, ignore_index=True)
	
	
res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBurLev2Orgs20120813V1.0.csv')

=
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