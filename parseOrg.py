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
		#need to deal with advertising pages and any other pages missing -ANNOYING NEED TO FIND A BETTER WAY
		#if they aren't one page before a missing number go ahead and caluclate normally
		if (bur['pageNum'] not in [num - 1 for num in [48, 49, 62, 63, 93, 94, 234, 304]]) or bur['pageNum'] == bur['pageNumEnd']:
			distance = pnClose - pnOpen #how many pages there are we need to grab
		else:
			if (bur['pageNum'] == 47 or bur['pageNum'] == 61 or bur['pageNum'] == 92):
				distance = (pnClose - pnOpen) - 2
				print(distance, bur['org'])
				input("ENTER")
			elif bur['pageNum'] == 233 or bur['pageNum'] == 303:
				distance = (pnClose - pnOpen) - 1 #how many pages there are we need to grab
				print(distance, bur['org'])
				input("ENTER")
		start = bur['span'][0] #find the beginning of the entry
		bur['content'] = str("") 
		print("Original distance", distance)
		def recursePages(distance,begin, pageCount):
			if distance == 0: # if the whole entry is on one page
				print("I entered this DISTANCE0 or loop here")
				print(bur['content'])
				#add a slice which spans until the next entry on the last page needed to be evaluated
				bur['content'] = bur['content'] + pnEntries[pageCount]['content'][begin:burEntries[b+1]['span'][0]]
				#print(bur['content'])
			else:
				#if not get the page from wherever the last entry left off (or the beginning if it's the second time around) to the end
				bur['content'] = bur['content'] + pnEntries[pageCount]['content'][begin:len(pnEntries[pageCount]['content'])]
				begin = 0
				distance = distance-1
				pageCount +=1
				#print(bur['content'])
				print(distance)
				#input("")
				recursePages(distance,begin,pageCount)
		for p, page in enumerate(pnEntries):
			if page['pageNum'] == bur['pageNum']: #get that page
				pageCount = p
				recursePages(distance, start, pageCount)
	burEntries[-1]['content'] = pnEntries[-1]['content'][burEntries[-1]['span'][0]:len(pnEntries[-1]['content'])-1] #deal with the last page separately
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