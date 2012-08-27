#!/usr/bin/env python
# encoding: utf-8
"""
Demonstration code for a suite functions to parse bibliographic data from books
"""
import os
import pandas as pd
import functools
import operator
import copy
import regex
path = str('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/')

#1
# The fist step is to get a set of dictionaries with the contents of each page
#-Done with getPages()
#the document must be saved with option to preserve pagebreaks in Abby Lingvo checked
pnEntries = getPages(path + 'gouv2011.003V3.1LineBreaksParagraphSeparator.txt')	

#2
#The next step is to get a set of index entries
#Entries could be from the table of contents, which currently returns a dictionary with two levels
#It can be done from the index as well
#indices should be saved with no headers or footers for proper parsing
#unfortunately there are long and short names for the ministry and this does not catch the whole name
toc = getLevelsTOC(path + "toc2011.001V1.2.txt")
lev1 = copy.deepcopy(toc['lev1']) #there is a different between a shallow and a deep copy. Shallow allows you to add to mutable objects
lev2 = toc['lev2']

#currently I through out two indices because they don't match, but could fix that. 
indices = getLevelsIndex('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentralesV1.4.txt')
indicesBup = copy.deepcopy(indices)
#3
#The next step is to find the bureacratic organizations' names in the text
#this is done with matchBurLev()
#this maybe potentially be recursively for each level of the bureacracy but I have found it impossible fo far
#insread we just match for all levels and combined them
burEntries = matchBurLev(pnEntries, lev1)
burEntriesIndex = matchBurLev(pnEntries, indices) #this doesn't work the first time around... not sure why but when the element are popped it workds
burEntriesIndexBup = copy.deepcopy(burEntriesIndex)
#burEntriesIndex = copy.deepcopy(burEntriesIndexBup)
be = sorted(burEntries +burEntriesIndex, key=operator.itemgetter('pageNum', 'end')) #sorted by both so they get called properly by parseOrg
beBup = copy.deepcopy(be)
#be = copy.deepcopy(beBup)
#4
#The next step is to get all of the text associated with apprpriate bureaucratic organization.
#Maybe this will be need to be called recursively if organizations are nested. 
#I believe there maybe a better strategy to detect level after all records are created because there is no abstractable code I can do that with
#burEntries2 = parseOrg(pnEntries, burEntries)
#burEntries[0] #yields the president
#combined ministerial level data nd index data
beEntriesT2 = parseOrg(pnEntries, be)


#5
#once all of the levels o bureacracy is matched - the remaining text will be parsed and old functions will be refactored for this
#to yield appropriate fields for appropriate levels. 
#Parses the data and actually retlevurns parsed records

myptest = feedData(beEntriesT2)

#this is a deep copy so i can compare
anotherTest = getSubOrgData(myptest)

# demonstration of text to output csv
# op2['entries']
# keys = ['loc','name', 'nameFlag', 'rank','email','tel','fax', 'title']
# res = pd.DataFrame(columns=keys)
# for q in range(0, len(op2['entries'])):
# 	row = pd.DataFrame((op2['entries'][q]), index = [q])
# 	res = res.append(row, ignore_index=True)
# 
# res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120812V2.21.csv')
for i in range(len(myptest)):
	print(myptest[i]['indEntries'],"\n",
	myptest[i]['org'], "ORG", "\n" ,
	myptest[i]['orgData'], "ORGDATA", "\n",
	myptest[i]['content'][0:200], "ORGDATA", "\n")
	input("ENTER")

###output individual level records
index = pd.DataFrame(columns=None)
i=1
for q, query in enumerate(anotherTest):
	for r, record in enumerate(query['indEntries']):
		myRow ={}
		myRow['rank'] = record['rank']
		
		myRow['email'] = str(record['email'])
		myRow['title'] = str(record['title'])
		myRow['tel'] = str(record['tel'])
		myRow['fax'] = str(record['fax'])
		myRow['org'] = query['org']
		if 'remainder' in record.keys():
			myRow['remainder'] = record['remainder']
		if 'name'  in record.keys():	
			myRow['name'] = record['name']
		if 'noParse'  in record.keys():	
			myRow['noParse'] = record['noParse']
		if 'subOrg'  in record.keys():	
			myRow['subOrg'] = record['subOrg']
		if 'subOrgData'  in record.keys():	
			myRow['subOrgData'] = record['subOrgData']
		if 'ministry' in query.keys():
			myRow['ministry'] = query['ministry'] 
		if 'level' in query.keys():
			myRow['level'] = query['level'] 
		print(myRow)
		row = pd.DataFrame((myRow), index = [i])
		index = index.append(row, ignore_index=True)
		print(row)
		i+=1

#index.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120825V1.1.csv')
 #index.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120825V1.2.csv')

# if it is the first record it can still have the next records data
#need to call each thing multiple time -- email twice -- DONE but doesn work
#doesn't work on last record
#title now doesn't match with comma
#title doesn't match across lines
, contre-amiral
 Sous-direction Pilotage
 des ressources humaines militaires
 et civiles
#Doesnot match tell and fax
Jean-Marie delarue
Tél. : 01 53 38 47 80 Fax : 01 42 38 85 32
##output remaindertest level records
remainder = pd.DataFrame(columns=None)
i=1
for q, query in enumerate(myptest):
	for r, record in enumerate(query['indEntries']):
		myRow = record
		myRow['org'] = query['org']
		print(myRow)
		row = pd.DataFrame((myRow), index = [i])
		remainder = remainder.append(row, ignore_index=True)
		print(remainder)
		i+=1

remainder.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120821REMAINDERTEST.csv')

###
for e, entry in enumerate(beEntriesT2):
	if entry['org'] =="Direction de l'énergie":
		print(entry['content'],"ORG=====" ,entry['org'], beEntriesT2[e+1]['org'], "NUMBER", e)

for e, entry in enumerate(beEntriesT2):
	if entry['org'] =="Service hydrographique et océanographique de la marine (SHOM)":
		print(entry['content'],"ORG=====" ,entry['org'], beEntriesT2[e+1]['org'], "NUMBER", e)

m
print(beEntriesT2[471]['content'])
print(beEntriesT2[472]['span'])
print(beEntriesT2[472]['pageNum'])



for e, entry in enumerate(anotherTest):
	if entry['org'] =="Cabinet du ministre":
		print(entry['content'],"ORG=====" ,entry['org'],e)
		input("ENTER")

for entry in pnEntries:
	if entry['pageNum'] == 235:
		print(entry['content'], "HEADER: ", entry['header'])
		
for entry in pnEntries:
	if entry['pageNum'] == 236:
		print(entry['content'], "HEADER: ", entry['header'])
		

###############-----------------------------------------------------------------------------------------
# orgs = [item['org'] for item in lev1]
# 	
# 	
# for org in orgs:
# 	for i in lev2:
# 		if i['lev1Org'] == org:
# 			print(org, i['org'])
# 	print("ORG BREAK__________")		
# 		
# "Ministre chargé" - in ministry but not reporting to the minister
# "SECRETAIRE D'ÉTAT" in ministry but not reporting to the minister
# 
# "Haute functionnaire" - reports directly to minister - not in toc comes after any Ministre chargé
# "Inspection générale" - reports directly to minister - not in toc
# "Secrétariat générale" - in MFA reports directly to minister and responsible for all general 2nd tier government agencies in other ministries
# 
# 
# 
# "service de controle budgetaire" --always free floating
# 
# #things in table of conents with uknown location in the hierarchy but not in organigrams
# "Services rattachés"
# "Organismes rattachés"
# "Ambassades et missions diplomatiques"
# "Services"
# "Établissements publics" -- or anything with the world establissement
# 
# 
# def tokenize2(source):
#     search = re.compile(r'([^;#\n]+)[;\n]?(?:#.+)?', re.MULTILINE)
#     for match in search.finditer(source): #re.iter iterates through the text fo find matchs and returns 
#         for item in match.groups():
#             yield item

#Direction with no sub-direction not in table of contents -- three in MFA?
#does Bureau de cabinet report directly to the minister? sometimes yes, sometimes now but neither are in TOC
#sometimes titles are longer in the doc then they are in the TOC