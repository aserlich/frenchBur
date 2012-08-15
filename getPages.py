#!/usr/bin/env python
# encoding: utf-8
"""
getPN.py

Created by Aaron Erlich on 2012-08-07.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""
import sys
import os

def getPages(fileName):
	"""
	Finds the footers for each page of a book and returns the page number and the location
	in the text associated with the beginning and end of the page and that contents
	Currently implemented for 2011. Will be made more generic as volum
	"""
	import functools
	fh = open(fileName)
	x = fh.readlines()
	pnO = regex.compile(r'#\s?([1-9][0-9]{0,2})', flag = regex.UNICODE) #for finding the odd pages
	pnE = regex.compile(r'^\s?([1-9][0-9]{0,2})\s?#', flag = regex.UNICODE) #for finding the even pages
	#pnE = regex.compile(r'', flag = regex.UNICODE)
	#pns =  []
	#locs = []
	pnEntries = []
	for i in range(0, len(x)):
		m = regex.search(pnO, x[i]) 
		n = regex.search(pnE, x[i]) 
		if m != None:
			#print(int(m.group(1)))
			#pns.append(int(m.group(1)))
			#locs.append(i)
			ref={}
			ref['pageNum'] = int(m.group(1))
			ref['endLoc'] = i
			pnEntries.append(ref)	
		elif n!= None:
			#pns.append(int(n.group(1)))
			#print(n.group(1))
			#locs.append(i)
			ref={}
			ref['pageNum'] = int(n.group(1))
			ref['endLoc'] = i
			pnEntries.append(ref)
	def addEndLoc(pnEntries):
		pnEntries = sorted(pnEntries, key=operator.itemgetter('endLoc')) #sort the dictionary of page numbers
		start = 0 #start starts at the start of the first page
		for page in pnEntries:
			if 'endLoc' not in page.keys():
				print("Error: you are missing an endLoc asociated with a page")
			else:
				page['startLoc'] = start
				start = page['endLoc'] + 1
	def addPages(pnEntries):
		for i, page in enumerate(pnEntries):
			page['content'] = functools.reduce(lambda x,y: x +" " + y, [line[:-1] for line in x[page['startLoc']:page['endLoc']]]) 
	addEndLoc(pnEntries)
	addPages(pnEntries)
	return(pnEntries)

#To implement later are tests -- this tests 
pns = getPages('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V3.0.txt')	
# nums = [item['pageNum'] for item in pns ]
# sorted(set(range(40,414)) -set(nums))
# sorted(set(nums) - set(range(40,413)))	
# #[48, 49, 62, 63, 93, 94, 234, 304]
# #48,49,62,63 are blank section break pages and omitted
# #need to rescan 93,94 
# #304 and 234 are is ad page omitted
