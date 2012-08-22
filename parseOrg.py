#!/usr/bin/env python 
# encoding: utf-8
"""
parseOrg.py

Created by Aaron Erlich on 2012-08-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import pdb
def parseOrg(pnEntries, burEntries):
	""""
	Transforms text parsed by page to text parsed by bureaucratic level
	Recursively implemented to keep on looking through more pages until all the content is found
	"""
	for b, bur in enumerate(burEntries[:-1]): #use enumerate so I can look forward
		#print(bur)
		pnOpen= bur['pageNum'] #page is an int
		pnClose = burEntries[b+1]['pageNum'] #get the page number where the entry closes, which is on the next entry only if the entry is sorted by page number and endloc
		print(pnOpen)
		print(pnClose)
		#pdb.set_trace()
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
						print(bur['content'])
						bur['content'] = bur['content'] + pnEntries[p]['content'][start:burEntries[b+1]['span'][0]] #on one page
						#print(bur['content'])
					else:
						bur['content'] = bur['content'] + pnEntries[p]['content'][bur['span'][0]:len(pnEntries[p]['content'])] #if not get the page from its start to the end
						start = 0
						distance = distance-1
						p += 1
						#print(bur['content'])
						print(distance)
						print(p)
						#input("")
						recursePages(distance,start,p)
				recursePages(distance, start, p)
	burEntries[-1]['content'] = pnEntries[-1]['content'][burEntries[-1]['span'][0]:len(pnEntries[-1]['content'])-1]
	burEntries[-1]['pageNumEnd'] = pnEntries[-1]['pageNum']
	return(burEntries)
	
##This was an attempt to get the data hiearachically -- it was unsucessful to date
# def parseOrg2(burEntries, indexEntries):
# 	i = 0
# 	for m, mnstry in enumerate(burEntries[:-1]): #deal with last separate
# 		lev1Index = []
# 		lev2Index =[]
# 		special = 0
# 		if i > 0 :
# 			if indexEntries[i]['pageNum'] == indexEntries[i-1]['pageNum']: #currently problem if index entry is on more than one page
# 				i -= 1
# 				special = 1
# 		while  indexEntries[i]['pageNum'] in range(mnstry['pageNum'], mnstry['pageNumEnd']+1): #if its in that 
# 			asRE1 = regex.escape(indexEntries[i]['org'].strip().upper(), regex.UNICODE)
# 			pattern1 = "\\s(?:(" + asRE1 +")"+ '{s<=3, i<=1, d<=1})' 
# 			myreg1 = regex.compile(pattern1,  regex.UNICODE + regex.VERSION1 + regex.FULLCASE)
# 			asRE2 = regex.escape(indexEntries[i]['org'].strip(), regex.UNICODE) #escape only create a string
# 			pattern2 = "\\s(?:(" + asRE2 +")"+ '{s<=3, i<=1, d<=1})' 
# 			myreg2 = regex.compile(pattern2, regex.UNICODE + regex.VERSION1 + regex.FULLCASE) #when compile with flags 
# 			i +=1
# 			if myreg1.search(mnstry['content'], regex.ENHANCEMATCH | regex.BESTMATCH) !=None:
# 				myMatch =myreg1.search(mnstry['content'], regex.ENHANCEMATCH | regex.BESTMATCH)
# 				#print(myMatch)
# 				tempEntry ={}
# 				tempEntry['span'] = myMatch.span(1)
# 				tempEntry['end'] = myMatch.end(1)
# 				tempEntry['org'] = indexEntries[i]['org']
# 				tempEntry['level'] = 1
# 				#print(indexEntries[i])
# 				lev1Index.append(tempEntry)
# 				print(tempEntry, mnstry['org'])
# 				input("")
# 			elif myreg2.search(mnstry['content'],  regex.ENHANCEMATCH | regex.BESTMATCH | regex.IGNORECASE) !=None:
# 				myMatch =myreg2.search(mnstry['content'], regex.ENHANCEMATCH | regex.BESTMATCH | regex.IGNORECASE)
# 				#print(myMatch)
# 				tempEntry2 ={}
# 				tempEntry2['span'] = myMatch.span(1)
# 				tempEntry2['end'] = myMatch.end(1)
# 				tempEntry2['org'] = indexEntries[i]['org']
# 				tempEntry2['level'] = 2
# 				lev2Index.append(tempEntry2)
# 				print(indexEntries[i], "SUCCESSFULLY MATCHED IN", mnstry['org'])	
# 			elif special !=1:
# 				print(indexEntries[i], "DIDN\'T MATCH IN", mnstry['org'])	
# 		mnstry['lev1Index'] = lev1Index
# 		mnstry['lev2Index'] = lev2Index
# 		#print("LEVEL 2 INDEX:", mnstry['lev2Index'], "LEVEL 1 INDEX:", mnstry['lev1Index'])
# 	return(burEntries)
# 
# 
# #sometimes parentheses are there sometimes they are not
# #sometimes level 2s are no capitalized
# #need to fugre out a way to capture those not evaluated twice
# test = parseOrg2(burEntries2, indices)	
# 		#get all the entries that are in that ministry
# 		#match and sort locations
# 		#get level orgs -- they are capitalized
# 		#assume all else is lower then level 1 and grabe them 
# 
# for i in range(40,len(test)):
# 	print("LEV 2", '\n', test[i]["lev2Index"], '\n\n')
# 	print("LEV1", '\n', test[i]["lev1Index"], '\n'"ORG is", test[i]["org"], "on PAGES", test[i]['pageNum'])
# 	input(" ")
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