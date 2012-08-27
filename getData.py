#!/usr/bin/env python
# encoding: utf-8
"""
getData.py

Created by Aaron Erlich on 2012-08-20.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os


def feedData(entries):
	for e, entry in enumerate(entries):
		entry['indEntries'] = getData(entry['content'], entry)
	return(entries)


def getData(content, entry):
	names = regex.compile(r"""(^\s?
							(?:
								(?:
								(?!Secteur|Mission|Bureau|Télédoc|Télécopie|Site|Contact|Groupe|France 	#negative look behind for these words
									|Cellule|Délégation|Mission|Département|Centre|Télécom|Fonds|Iles
									|Valletta|Bâtiment|Secteur|Projet|Sous-direction|Section|Pôle
								)
								(?:[\p{Lu}] 										#first letter of first name is capitalized
									(?:[\p{Ll}]{2,15}){s<=1}						#then more letters all lowercase 
									(?:[\p{Pd}][\p{Lu}](?:[\p{Ll}]+){s<=2}\s|\s)	#then the possibility of a hyphenated name or just a space
								)
								(?:(?:
									(?:	(?!MINISTRE|AUTORITÉ|ÉTABLISSEMENTS|SECRÉTAIRE|ORGANISMES)										#Begin last name
									(?:[\p{Lu}]										#last name starts with a cap
										(?:[[\p{Pd}\p{Lu}\']--[,]]{3,23}){s<=1}		#then either an apostrophe uppercase letters or dashes
									)|(?:DE|DI|DA|DU|LE|LA)								#or one of the two letter names
								),?[\s\n]\s?){1,6})									#end last name and say it can be repeated 1 to 6 times		
							)														#end the name	
						|N\.\.\.)													#there can also be a N...
					)""", regex.VERBOSE + regex.UNICODE + regex.V1 + regex.MULTILINE) #multline used to capture multiple records
	title = regex.compile(r"""
								^,?\ ?(												#can start with a comma which sometimes separates from a name needs to be cleaned later
									(?:
										(?:[\p{Ll}][[\p{Ll}\-']--[@:\.]]{1,})\s		#a word with no caps or garbage
										(?:
											(?:
												(?:[\p{Ll}][[\p{Ll}\-']--[@:\.]]{1,})|
												(?:à|a|Affaires|Banque\ de\ France|Cour|CTC|DGCCRF|d\'État|France				#exceptions of capitalized words
												|l\'iNSEE|l\'INSEE
												|l\'Assemblée|l\'Académie|l\'Enseignement|l'État
												|Paris|République|TPE|Trésor
												)
										),?[\ \n]{1}\s?){0,12}					#after each word there can be a comma followed by either space or a line break
									)
								   )""", regex.UNICODE + regex.VERBOSE +regex.V1)
	#insertions to deal with blank spaces or linebreaks and period at the end is option as often not caught
	email = regex.compile(r'^(?:([a-zA-Z0-9+.\-\']+@[a-z0-9.\-]+\.?(?:fr|com|eu|org|net)){i<=2})', regex.UNICODE |regex.V1) 
	tel = regex.compile(r'^(?:Tél\.?\s*:\s*\+*((?:[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	fax = regex.compile(r'^(?:Fax\s*:\s*((?:\+*[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	regexes = [("title",title), ("email", email), ("tel", tel), ("fax",fax)] #a list of tuples
	#print(regexes)
	#orgData = indEntries[0] 
	entries =[]
	indEntries = content.split('•') #parse by individual entry (or everyone with the same position) before the first split will be org level data
	entry['orgData'] = indEntries[0]
	for e in range(1, len(indEntries)):
		keys = ['email','tel','fax', 'title']
		dentry= {key: [] for key in keys}
		allInfo = indEntries[e].split(':', 1) #split on the first semicolon before will be the rank
		print(allInfo, "ALL INFO")
		
		if len(allInfo) ==2:
			dentry['rank'] = allInfo[0].strip()
			otherInfo = names.split(allInfo[1].lstrip()) #get the rank
			print(otherInfo, "whose LENGTH is:", len(otherInfo))
			#input("")
			
			if len(otherInfo) == 3: #if we got a proper name split
				dentry['name'] = otherInfo[1].strip()
				otherInfo = otherInfo[2].lstrip()	
				matchCoord(regexes, dentry, otherInfo)
				entries.append(dentry)
				
			elif len(otherInfo) == 1: # we didn't sucssefully split
			#For error checking of likely names but ones outside the tolerance threshold given by the regex but I still want to parse
				potentialName = otherInfo[0].split("\n",1)[0].split(" ")	
				if len(potentialName) <= 2:
					dentry['name'] = ' '.join(potentialName)
					dentry['nameFlag'] = 1
					potentialOtherInfo = otherInfo[0].split("\n",1)
					if len(potentialOtherInfo) == 2:
						matchCoord(regexes, dentry, potentialOtherInfo[1])
				entries.append(dentry)
				
			elif len(otherInfo) > 3:  #we have multiple names
				print('LONG SPLIT')
				##DEAL with the first entry
				dentry['name'] = otherInfo[1].strip()
				if names.match(otherInfo[2]) == None: #if the next cell isn't a name
					matchCoord(regexes, dentry, otherInfo[2].lstrip())
					rangeStart = 3
				else: 
					rangeStart ==2
				#now for all other entries
				for stray in range(rangeStart, len(otherInfo)): #either 2 or 3 depending
					if names.match(stray) != None: #if the next element isn't name
						newEntry= {key: [] for key in keys}
						newEntry['rank'] = dentry['rank']
						newEntry['name'] = stray.strip() #this means there was no material between the two names
					else:
							matchCoord(regexes, newEntry, extras[1].lstrip())
							entries.append(newEntry)
				entries.append(dentry)
				input(" ")
			else: # we didn't sucssefully split
				print(otherInfo, "IS AN ERROR BECAUSE THERE IS NO NAME")
				dentry['nameFlag'] = 2
				dentry['noParse'] = otherInfo #shove all the info about the record into 1 string
				
		else:
			print("There is a problem with rank parsing:\n", allInfo, "\n",
			content)
			otherInfo = allInfo
			#input("ENTER")
	return(entries)	

x= getData(beEntriesT2[12]['content'], beEntriesT2)

def matchCoord(regexList, recordEntry, info):
	import regex
	info = info
	for r, myreg in enumerate(regexList):
		splitInfo = myreg[1].split(info.lstrip())
		if len(splitInfo) == 3:
			print(myreg[0], splitInfo[1].lstrip())
			recordEntry[myreg[0]].append(splitInfo[1].strip())
			print(info, "HERE AFTER STRIP", "and R =", r)
			#matchCoord([myreg], recordEntry, splitInfo[2]) #call recursively to get double phone number or emails or faxes NEED TO MAKE WORK PROPERL
			info = splitInfo[2].lstrip()
	if info:
		recordEntry['remainder'] = info
		print("REMAINDER", recordEntry['remainder']) #this needs ot be expanded to do a bit of testing for being a lower level of bureaucracy on the next record		

def getSubOrgData(entries):
	import copy
	test = copy.deepcopy(entries) #make a copy
	for e, entry in enumerate(test):
		for i, indEntry in enumerate(entry['indEntries']):
			if e != len(test)-1:  #if its not the last entry
				if 'remainder' in indEntry.keys():
					orgParse = recurseRemainder(indEntry['remainder'])
					if orgParse[0] != None and len(orgParse[0])>0:
						if i == len(entry['indEntries'])-1: #if its the last individual entry, data goes with next entry
							#pri	nt(i, len(indEntry))
							print(e)
							test[e+1]['indEntries'][0]['subOrg'] = orgParse[0]
							test[e+1]['indEntries'][0]['subOrgData'] = orgParse[1]
							del(indEntry['remainder'])
						else:
							print(i, len(indEntry))
							test[e]['indEntries'][i+1]['subOrg'] = orgParse[0]
							test[e]['indEntries'][i+1]['subOrgData'] = orgParse[1]
							del(indEntry['remainder'])
					print(orgParse)
		for i, indEntry in enumerate(entry['indEntries']):
			if i >0:
				if 'subOrg' not in indEntry.keys() and 'subOrg' in entry['indEntries'][i-1].keys():
					print(entry['indEntries'][i])
					indEntry['subOrg'] = entry['indEntries'][i-1]['subOrg']
					indEntry['subOrgData'] = entry['indEntries'][i-1]['subOrgData']
	return(test)


def recurseRemainder(remainder, nonOrg = "", orgMatch=None):
	org = regex.compile(r"(^[\p{Lu}](?:[[\p{Ll}\p{Lu}\-\'\(\),\s]--[\d:@\.]]+$))", regex.UNICODE + regex.V1) #but sometimes there are : and numbers but usually just one
	if org.match(remainder) : #if it just has org details
		orgMatch = org.match(remainder).group(1) #assign it to the org
		print(orgMatch, "ORGMATCH", nonOrg)
		return(orgMatch, nonOrg)
	elif len(remainder.rsplit("\n",1)) ==2:
			nonOrg = nonOrg + remainder.rsplit("\n",1)[1]
			return(recurseRemainder(remainder = remainder.rsplit("\n",1)[0], nonOrg = nonOrg)) #need to return it here
	else: 
		orgMatch = None
		return(orgMatch, nonOrg)

			#have to attached it to the right entry
# mt = getData(ltest)		
# rt = getData(rtest)	

website = regex.compile(r'^www\..*\.[\p{Ll}]{2,3}', regex.UNICODE + regex.V1)

webstrings = ["www.minister.gouv.fr and some other stuff", "aaronerlic@gmail.com"]
