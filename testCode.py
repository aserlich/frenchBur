#!/usr/bin/env python
# encoding: utf-8
"""
Demonstration code for a suite functions to parse bibliographic data from books
"""
import os
path = str('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/')

#1
# The fist step is to get a set of dictionaries with the contents of each page
#-Done with getPages()
#the document must be saved with option to preserve pagebreaks in Abby Lingvo checked
pnEntries = getPages(path + 'gouv2011.003V3.1LineBreaks.txt')	

#2
#The next step is to get a set of index entries
#Entries could be from the table of contents, which currently returns a dictionary with two levels
#It can be done from the index as well
#indices should be saved with no headers or footers for proper parsing
toc = getLevelsTOC(path + "toc2011.001V1.2.txt")
lev1 = toc['lev1']
lev2 = toc['lev2']
indices = getLevelsIndex('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentralesV1.4.txt')

#3
#The next step is to find the bureacratic organizations' names in the text
#this is done with matchBurLev()
#this maybe potentially be recursively for each level of the bureacracy but I have found it impossible fo far
#insread we just match for all levels and combined them
burEntries = matchBurLev(pnEntries, lev1)
burEntriesIndex = matchBurLev(pnEntries, indices)
be = sorted(burEntries +burEntriesIndex, key=operator.itemgetter('pageNum'))

#4
#The next step is to get all of the text associated with apprpriate bureaucratic organization.
#Maybe this will be need to be called recursively if organizations are nested. 
#I believe there maybe a better strategy to detect level after all records are created because there is no abstractable code I can do that with
burEntries2 = parseOrg(pnEntries, burEntries)
burEntries[0] #yields the president
#combined ministerial level data nd index data
beEntriesT2 = parseOrg(pnEntries, be)


#5
#once all of the levels o bureacracy is matched - the remaining text will be parsed and old functions will be refactored for this
#to yield appropriate fields for appropriate levels. 
#Parses the data and actually returns parsed records

myptest = feedData(beEntriesT2)
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
	myptest[i]['conten'][0:20], "ORGDATA", "\n")
	input("ENTER")

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