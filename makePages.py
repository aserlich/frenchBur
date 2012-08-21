#!/usr/bin/env python
# encoding: utf-8
"""
makePages.py
Created by Aaron Erlich on 2012-08-12.
"""
#currently not needed since folded into getPages()
# import sys
# import getopt
# 
# def makePages(pnEntries, fileName):
# 	"""
# 	creates a dictionary of pages and all the text associated with each page
# 	"""
# 	import functools
# 	import operator
# 	fh = open(fileName)
# 	x = fh.readlines()
# 	pnEntries = sorted(pnEntries, key=operator.itemgetter('pageNum'))
# 	for pnpage in pnEntries : #for every page in the book
# 		oneLine = functools.reduce(lambda x,y: x +" " + y, [line[:-1] for line in x[pnpage['startLoc']:pnpage['endLoc']]]) 
# 		pnpage['contents'] = oneLine
# 	return(pnEntries)
# 
# pages = makePages(op2['pageNums'], '/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003V2.4.txt')

