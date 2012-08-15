#!/usr/bin/env python
# encoding: utf-8
"""
chunkInst.py

Created by Aaron Erlich on 2012-08-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys

def parseOrg(pnEntries, burEntries):
	""""
	Transforms text parsed by page to text parsed by bureaucratic level
	Recursively implemented to keep on looking through more pages until all the content is found
	"""
	for b, bur in enumerate(burEntries[:-1]): #use enumerate so I can look forward
		#print(bur)
		pnOpen= bur['pageNum'] #page is an int
		pnClose = burEntries[b+1]['pageNum'] #get the page number where the entry closes, which is on the next entry
		print(pnOpen)
		print(pnClose)
		bur['pageNumEnd'] = pnClose #assign that to the dictionary entry
		distance = pnClose - pnOpen #how many pages there are we need to grab
		start = bur['span'][0]
		bur['content'] = str("")
		print("Original distance", distance)
		for p, page in enumerate(pnEntries):
			if page['pageNum'] == bur['pageNum']: #get that page
				def recursePages(distance,start, p):
					if distance == 0:
						print("I entered this DISTANCE0 or loop here")
						bur['content'] = bur['content'] + pnEntries[p]['content'][start:burEntries[b+1]['span'][0]] #on one page
						#print(bur['content'])
					else:
						bur['content'] = bur['content'] + pnEntries[p]['content'][bur['span'][0]:len(pnEntries[p]['content'])-1] #if not get the page from its start to the end
						start = 0
						distance = distance-1
						p += 1
						#print(bur['content'])
						print(distance)
						print(p)
						#input("")
						recursePages(distance,start,p)
				recursePages(distance, start, p)
	burEntries[-1]['content'] = pnEntries[-1]['content'][burEntries[-1]['span'][0]:len(pnEntries[-1]['contents'])-1]
	return(burEntries)
	
	
##oldversion non-recursive and not full inmplemented
# def chunkInst(indices, content):
# 	#sort 
# 	for i, item in enumerate(indices[:-1]): #use enumerate so I can look forward
# 		pnOpen= item['pageNum']
# 		print(pnOpen)
# 		for page in content:
# 			#print(page)
# 			if 'pageNum' in page and page['pageNum'] == pnOpen:
# 				pnClose = indices[i+1]['pageNum']
# 				if pnClose == pnOpen:
# 					item['chunk'] = page['contents'][item['span'][0]:indices[i+1]['span'][0]]
# 					#print(item['chunk'])
# 					#input("")
# 	indices[-1]['chunk'] = content[-1]['contents'][indices[-1]['span'][0]:len(content[-1]['contents'])-1]
# 	return(indices)				