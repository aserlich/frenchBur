#!/usr/bin/env python
# encoding: utf-8
"""
getPN.py

Created by Aaron Erlich on 2012-08-07.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""
import sys
import os

def getPN(fileName):
	"""pn
	Finds the footers for each page of a book and returns the page number
	Currently implemented for 2011.
	"""
	fh = open(fileName)
	fh.seek(0)
	x = fh.readlines()
	pnO = regex.compile(r'#\s?([1-9][0-9]{0,2})', flag = regex.UNICODE)
	pnE = regex.compile(r'^\s?([1-9][0-9]{0,2})\s?#', flag = regex.UNICODE)
	#pnE = regex.compile(r'', flag = regex.UNICODE)
	pns =  []
	locs = []
	PNentries = []
	for i in range(0, len(x)):
		m = regex.search(pnO, x[i]) 
		n = regex.search(pnE, x[i]) 
		if m != None:
			#print(int(m.group(1)))
			pns.append(int(m.group(1)))
			locs.append(i)
			ref={}
			ref['pageNum'] = int(m.group(1))
			ref['loc'] = i
			PNentries.append(ref)	
		elif n!= None:
			pns.append(int(n.group(1)))
			#print(n.group(1))
			locs.append(i)
			ref={}
			ref['pageNum'] = int(n.group(1))
			ref['loc'] = i
			PNentries.append(ref)	
	return(PNentries)

#To implement later are tests
#pns = getPN('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V1.3.txt')	
#set(range(64,413)) -set(pns)
#set(pns) - set(range(64,413))	
#{304, 234, 93, 94}	
#need to rescan 93,94 
#304 and 234 are is ad page omitted
