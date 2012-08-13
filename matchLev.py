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
	PNDict = sorted(PNDict, key=operator.itemgetter('endLoc')) #sort the dictionary of page numbers
	#print(PNDict)
	counter = 0
	start = 0
	for dictio in PNDict: #go through every page number
		print(dictio)
		dictio['startLoc'] = start #set the start location of the page to start
		while entDict[counter]['loc'] in range(start, dictio['endLoc']): #while we are still on the page make that entry in the dictionary have the page
			entDict[counter]['pageNum'] = dictio['pageNum']
			if counter < len(entDict)-1:
				counter += 1
			else:
				break
			print(counter)	
		start = dictio['endLoc']+1
		#print(i)
		print(start)

#sys.path.append('/Library/Python/diff_match_patch_20120106/python3')
#import diff_match_patch

def matchBurLev(evalLines, entDict, indexDict, PNDict, fileName):
	"""
	
	"""
	import functools
	#import functools
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
		for pnpage in PNDict : #for every page in the book
			if int(indpage['pageNum']) == int(pnpage['pageNum']) and int(indpage['pageNum']) in range(minVal, maxVal+1): 
				print("Got PN")
				asRE = regex.escape(indpage['nameOnly'].strip(), regex.UNICODE)
				pattern = "(" + asRE +")"+ '{e<=3}' 
				print(pattern)
				instMatch = regex.search(pattern, pnpage['contents'],regex.ENHANCEMATCH | regex.BESTMATCH | regex.BESTMATCH | regex.IGNORECASE | regex.UNICODE | regex.V1)
				if instMatch != None:
					print(instMatch.group(1),  instMatch.span(1))
					indpage['instMatch'] = instMatch.group(1)
					indpage['span'] = instMatch.span(1)
					indpage['end'] = instMatch.end(1)
				#gdiff = dmp.diff_match_patch()
				#location = gdiff.match_main(oneLine.lower(), indpage['nameOnly'].lower(), 0)
				#print(location)
				#print(indpage['nameOnly'])
				
				elif int(indpage['pageNum']) not in range(minVal, maxVal+1):
					indpage['instMatch'] = None
					indpage['span'] = None
					indpage['end'] = None
				else:
					print(pattern, "did not match") 
					indpage['instMatch'] = None
					indpage['span'] = None
					indpage['end'] = None
				#input("")
	return(indexDict)

xmod = getLevels('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentralesV1.3.txt')
op2 = firstPass('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V2.4.txt')
test1 = matchBurLev(op2['evalLines'], op2['entries'], xmod['indEntries'], op2['pageNums'], '/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V2.4.txt')

probs =[]
for d in test1:
	if 'instMatch' in d:
		if d['instMatch'] == None and d['pageNum'] >= 64:
			print(d)
			probs.append(d)

a=[]
for items in test1:
	if 'end' in items and items['end'] !=None:
		a.append(items)
	elif 'end' not in items:
		print(items)
	
# a = sorted(test1, key=sortkeypicker(['pageNum', 'end']))
# 
# a = multikeysort(test1, ['pageNum', 'end'])
# a = multikeysort(test1, ['pageNum'])

import operator
a.sort(key=operator.itemgetter('pageNum', 'end')


def chunkInst(indices, content):
	#sort 
	for i, item in enumerate(indices[:-1]): #use enumerate so I can look forward
		pnOpen= item['pageNum']
		print(pnOpen)
		for page in content:
			#print(page)
			if 'pageNum' in page and page['pageNum'] == pnOpen:
				pnClose = indices[i+1]['pageNum']
				if pnClose == pnOpen:
					item['chunk'] = page['contents'][item['span'][0]:indices[i+1]['span'][0]]
					#print(item['chunk'])
					#input("")
	indices[-1]['chunk'] = content[-1]['contents'][indices[-1]['span'][0]:len(content[-1]['contents'])-1]
	return(indices)				


test2 = chunkInst(a, op2['pageNums'] )


l=[1,2,3]
for i,item in enumerate(l):
	print(i,item)
	if item==2:
		get_previous=l[i-1]
		print(get_previous)

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


gdiff = dmp.diff_match_patch()
gdiff.match_main("abc12345678901234567890abbc", "abc", 26)

# s1 = difflib.SequenceMatcher(None,x[line].strip().lower() , indpage['fullName'].strip().lower())
# if s1.ratio() == 1:
# 	print("We have a match: FILE",  x[line].strip().lower(), "\n INDEX", indpage['fullName'].strip().lower())
# 	indpage['startLoc'] = line
# 	input('Perfect')
# 	break
# elif s1.ratio() <1 and s1.ratio() > .6:
# 	line2 = line+1
# 	twolines = " ".join([x[line2].strip().lower(),x[line].strip().lower()]) #make this a lambda next
# 	s2 = difflib.SequenceMatcher(None, twolines , indpage['fullName'].strip().lower())
# 	if s2.ratio() > s1.ratio() and s2.ratio() >.6:
# 		print("We have a match: FILE", twolines, "\n INDEX", indpage['fullName'].strip().lower(), s2.ratio(), s1.ratio(), ":RATIOS")
# 		input(" ")
# elif s1.ratio() > .8:
# 	print("We have a match: FILE",  x[line].strip().lower(), "\n INDEX", indpage['fullName'].strip().lower(), "S! RATIO:", s1.ratio())
# 	print(line)
# 	input("")
# elif line == int(pnpage['loc']):