#!/usr/bin/env python
# encoding: utf-8
"""
matchBurLev.py

Created by Aaron Erlich on 2012-08-14.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os

def matchBurLev(pnEntries, indexEntries):
	"""
	Match the bureacratic level given in the text with the page number it is found on
	"""
	import functools
	minVal = min(item['pageNum'] for item in pnEntries) #lowest page number evaluated
	maxVal = max(item['pageNum'] for item in pnEntries) #highest page number evaluated
	for e, entry in enumerate(indexEntries): #for every entry in the index
		for p, page in enumerate(pnEntries): #for every page in the book
			if entry['pageNum'] == page['pageNum'] and entry['pageNum'] in range(minVal, maxVal+1): 
				print("Got PN")
				asRE = regex.escape(entry['org'].strip(), regex.UNICODE)
				words = asRE.split(" ")
				words = [word +regex.escapte("\n?") for word in words]
				asRE = ' '.join(words)
				pattern = "(" + asRE +")"+ '{e<=3}'
				print(pattern)
				#asRE = regex.escape(entry['org'].strip(), regex.UNICODE)
				#pattern = "(" + asRE +")"+ '{e<=3}' 
				print(pattern)
				instMatch = regex.search(pattern, page['content'],regex.ENHANCEMATCH | regex.BESTMATCH | regex.BESTMATCH | regex.IGNORECASE | regex.UNICODE | regex.V1)
				if instMatch != None:
					print(instMatch.group(1),  instMatch.span(1))
					entry['instMatch'] = instMatch.group(1)
					entry['span'] = instMatch.span(1)
					entry['end'] = instMatch.end(1)
				#gdiff = dmp.diff_match_patch()
				#location = gdiff.match_main(oneLine.lower(), entry['nameOnly'].lower(), 0)
				#print(location)
				#print(entry['nameOnly'])
				elif entry['pageNum'] not in range(minVal, maxVal+1):
					print("PageNum", entry['pageNum'], "out of Range")
					input("")
					indexEntries.pop(e)
					# entry['instMatch'] = None
					# entry['span'] = None
					# entry['end'] = None
				else:
					print(pattern, "did not match and was removed") 
					indexEntries.pop(e)
					# entry['instMatch'] = None
					# 			entry['span'] = None
					# 			entry['end'] = None
					input("Enter")
	indexEntries = sorted(indexEntries, key=operator.itemgetter('pageNum', 'end')) #key step to sort on BOTH pagenum and where the entry ends in the page
	return(indexEntries)