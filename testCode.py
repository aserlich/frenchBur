#!/usr/bin/env python
# encoding: utf-8
"""
Demonstration code for a suite functions to parse bibliographic data from books
"""
import os
path = str('/Volumes/Optibay-1TB/FrenchBur/2011/rawText')

# the fist step is to get a s set of dictionaries with the contents of each page
#- This is done with getPages()
pnEntries = getPages(path + 'gouv2011.003V3.0.txt')	

#the next step is to get a set of index entries
#this is from the table of contents, which currently returns a dictionary with two levels
#it can be done from the index as well
toc = getLevelsTOC(path + "toc2011.001V1.2.txt")
lev1 = toc['lev1']
lev2 = toc['lev2']

#the next step is to find the bureacratic organizations names in the text
#this is done with matchBurLev()
#this can be done recursively for each level of the bureacracy but I have done it with the highest right now
burEntries = matchBurLev(pnEntries, lev1)

#the next step is to get all of the text associated with that bureaucratic level. 
burEntries = parseOrg(pnEntries, burEntries)
burEntries[0] #yields the president

#once all of the levels o bureacracy is matched - the remaining text will be parsed and old functions will be refactored for this
# demonstration of text to output csv
# op2['entries']
# keys = ['loc','name', 'nameFlag', 'rank','email','tel','fax', 'title']
# res = pd.DataFrame(columns=keys)
# for q in range(0, len(op2['entries'])):
# 	row = pd.DataFrame((op2['entries'][q]), index = [q])
# 	res = res.append(row, ignore_index=True)
# 
# res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120812V2.21.csv')
