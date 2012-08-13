#!/usr/bin/env python
# encoding: utf-8
"""
matchLev.py

Created by Aaron Erlich on 2012-08-09.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

def matchPNDict(entDict, PNDict):
	"""
	Takes ina dictionary of all the page numbers and associates that page number with all of the lines of text on that page. 
	"""
	print("Entering matchPNDict")
	input("")
	import operator
	entDict = sorted(entDict, key=operator.itemgetter('loc'))  #sort the dictionary or entries
	PNDict = sorted(PNDict, key=operator.itemgetter('loc')) #sort the dictionary of page numbers
	#print(PNDict)
	counter = 0
	start = 0
	for dictio in PNDict: #go through every page number
		print(dictio)
		dictio['startLoc'] = start #set the start location of the page to start
		while entDict[counter]['loc'] in range(start, dictio['loc']): #while we are still on the page make that entry in the dictionary have the page
			entDict[counter]['pageNum'] = dictio['pageNum']
			if counter < len(entDict)-1:
				counter += 1
			else:
				break
			print(counter)	
		start = dictio['loc']+1
		#print(i)
		print(start)

def matchBurLev(evalLines, entDict, indexDict, PNDict, fileName):
	#entDict = sorted(entDict, key=operator.itemgetter('loc'))
	#indexDict = sorted(entDict, key=operator.itemgetter('pageNum'))
	fh = open(fileName)
	#fh.seek(0)
	x = fh.readlines()
	#print(x)
	#counter = 0
	#start = 0
	minVal = min(item['pageNum'] for item in entDict) #lowest page number evaluated
	maxVal = max(item['pageNum'] for item in entDict) #highest page number evaluated
	for indpage in indexDict: #for every entry in the index
		#print(ent)
		for pnpage in PNDict : #for every page in the book
			#print(dictio)
			#print(dictio['pageNum'])
			#testprint(indpage['pageNum']) #print the page the entry is on
			#input("")
			#if we are on the page of the index page
			if int(indpage['pageNum']) == int(pnpage['pageNum']) and int(indpage['pageNum']) in range(minVal, maxVal): 
				print("Got PN")
				print(range(int(pnpage['startLoc']), int(pnpage['loc'])))
				for line in range(int(pnpage['startLoc']), int(pnpage['loc'])): #get page of text
					lineNum = pnpage['startLoc']
					print(line)
					#print(x[line])
					#print(indpage['fullName'].lower())
					#input("")
					s1 = difflib.SequenceMatcher(None,x[line].strip().lower() , indpage['fullName'].strip().lower())
					if s1.ratio() == 1:
						print("We have a match: FILE",  x[line].strip().lower(), "\n INDEX", indpage['fullName'].strip().lower())
						indpage['startLoc'] = line
						input('Perfect')
						break
					elif s1.ratio() <1 and s1.ratio() > .6:
						line2 = line+1
						twolines = " ".join([x[line2].strip().lower(),x[line].strip().lower()]) #make this a lambda next
						s2 = difflib.SequenceMatcher(None, twolines , indpage['fullName'].strip().lower())
						if s2.ratio() > s1.ratio() and s2.ratio() >.6:
							print("We have a match: FILE", twolines, "\n INDEX", indpage['fullName'].strip().lower(), s2.ratio(), s1.ratio(), ":RATIOS")
							input(" ")
					elif s1.ratio() > .8:
						print("We have a match: FILE",  x[line].strip().lower(), "\n INDEX", indpage['fullName'].strip().lower(), "S! RATIO:", s1.ratio())
						print(line)
						input("")
					elif line == int(pnpage['loc']):
						indpage['startLoc'] == None
	return(indexDict)

test1 = matchBurLev(op2['evalLines'], op2['entries'], xmod['indEntries'], op2['pageNums'], '/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V2.3.txt')

for d in test:
	if 'loc' in d.keys() and d['loc'] == None:
		print(test)

probs =[]
for d in test1:
	if 'startLoc' not in d.keys()  and d['pageNum'] >= 64:
		print(d)
		probs.append(d)

(| 

import difflib
s = difflib.SequenceMatcher(None,"Agence de l'eau Lolre-Bretagne", "Agence de l'eau Loire-Bretagne and a lot of other text")
s.ratio()

def addInfo(indexDict):
	indexDict = sorted(indexDict, key=operator.itemgetter('startLoc')) #sort the dictionary of page numbers
	start =indexDict[0]['startLoc']
	for ind in range(0,len(indexDict)-1):
		if 'startLoc' in indexDict[ind].keys():
			indexDict[ind]['endLoc'] = indexDict[ind+1]['startLoc']-move

for i in test:
	print(i['startLoc'])

"Service des affaires financières, sociales et logistiques" in 'Service des affaires financières, sociales et logistiques (Agri. Alim.)' 

min(item['pageNum'] for item in op[0][02]
	
entDict = matchPNDict(op[2], pns[2])	
max(entDict, key =operator.itemgetter('pageNum'))

		
	difflib.SequenceMatcher(isjunk=None, a='', b='', autojunk=True)


123 = dict( name =' Bob Smith', age = 42, pay = 30000, job =' dev')
sue = dict( name =' Sue Jones', age = 45, pay = 40000, job =' hdw') 
#bob{'pay': 30000, 'job': 'dev', 'age': 42, 'name': 'Bob Smith'} 
db = {}  
db['bob'] = bob # reference in a dict of dicts 
db['sue'] = sue   
db['bob']['name'] # fetch bob's name 'Bob Smith' 
db['sue']['pay'] = 50000 # change sue's pay 
db['sue']['pay'] # fetch sue's pay 50000
