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
	import operator
	fh = open(fileName)
	x = fh.readlines()
	pnO = regex.compile(r'#\s?([1-9][0-9]{0,2})', flag = regex.UNICODE) #for finding the odd pages
	pnE = regex.compile(r'^\s?([1-9][0-9]{0,2})\s?#', flag = regex.UNICODE) #for finding the even pages
	header = regex.compile(r'(?:◄|►)', regex.UNICODE | regex.V1)
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
	def addStartLoc(pnEntries):
		pnEntries = sorted(pnEntries, key=operator.itemgetter('endLoc')) #sort the dictionary of page numbers
		start = 0 #start starts at the start of the first page
		for page in pnEntries:
			counter = 0
			if 'endLoc' not in page.keys(): #if there is no dictionary key with an endoc
				print("Error: you are missing an endLoc associated with a page, program terminated")
				break
			else:
				def headerSearch(start, page,counter):  #the start of the page should omit the word "gouvernment or other sideways words and the header"
					if header.search(x[start]) !=None:
						print(x[start], "\n", page['pageNum'])
						page['header'] = x[start].strip()
						page['startLoc'] = start+1 #omit the header
						print(page)
					else:
						counter +=1
						start +=1
						print(x[start], "in Recursion")
						#input("Enter")
						if counter < 4:
							headerSearch(start, page,counter)
						else:
							print("you are recursing too many levels. There is an error in the text")
							input("ENTER")
				headerSearch(start,page,counter)
				start = page['endLoc'] + 1
				print(start,page)
	def addPages(pnEntries): #actually adds the content of the page _ am snore we want to do this
		for i, page in enumerate(pnEntries):
			page['content'] = functools.reduce(lambda x,y: x +" " + y, [line for line in x[page['startLoc']:page['endLoc']]]) 
			#needs to be plus one or won't grap last line 
	addStartLoc(pnEntries)
	addPages(pnEntries)
	return(pnEntries)

#To implement later are tests -- this tests 
#pns = getPages('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V3.0.txt')	
# nums = [item['pageNum'] for item in pns ]
# sorted(set(range(40,414)) -set(nums))
# sorted(set(nums) - set(range(40,413)))	
# #[48, 49, 62, 63, 93, 94, 234, 304]
# #48,49,62,63 are blank section break pages and omitted
# #need to rescan 93,94 
# #304 and 234 are is ad page omitted
