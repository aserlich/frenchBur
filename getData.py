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
	names = regex.compile(r"""(^
								(?:
									(?:[\p{Lu}]
										(?:[\p{Ll}]{2,15}){s<=2}
										(?:[\p{Pd}][\p{Lu}][\p{Ll}]+\ |\ ){s<=1}
										(?:
											(?:
												(?:[\p{Lu}]
													(?:\'|[\p{Lu}]{2,15}){s<=1}
													(?:[\p{Pd}]['\p{Pd}\p{Lu}]{2,15})?
												)
											)|
											(?:DE|DI|DA|DU|LE|LA)
										)
										(?:
											(?:
												(?:\s[\p{Lu}])
												(?:\'|[\p{Lu}]{2,3})
												(?:[\'\p{Pd}\p{Lu}]{0,10})
											)|
											(?:\ DE|\ DU|\ LE|\ LA)
										){0,5}
									)
									|N\.\.\.)
								)[\s]?""", regex.VERBOSE | regex.UNICODE |regex.V1) #comma moved to title
	title = regex.compile(r"(^(?:(?:,?[\p{Ll}']{1,}[\s,])+)\n?)", regex.UNICODE) #dashes are still metacharacters inside classes
	email = regex.compile(r'^(?:([a-zA-Z0-9+.\-]+@[a-z0-9.\-]+\.(?:fr|com|eu|org)){i<=2})', regex.UNICODE |regex.V1) #insertions to deal with blank spaces or linebreaks
	tel = regex.compile(r'^(?:Tél\.?\s*:\s*\+*((?:[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	fax = regex.compile(r'^(?:Fax\s*:\s*((?:\+*[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	regexes = [title, email,tel, fax]
	#print(regexes)
	#orgData = indEntries[0] 
	entries =[]
	indEntries = content.split('•') #parse by individual entry before the first split will be org level data
	entry['orgData'] = indEntries[0]
	for e in range(1, len(indEntries)):
		dentry = {}
		allInfo = indEntries[e].split(':', 1) #split on the first semicolon before will be the rank
		print(allInfo)
		parsed =[None, None, None, None, None, None] #set up extra data spots could be used 
		if len(allInfo) ==2:
			dentry['rank'] = allInfo[0].strip()
			otherInfo = names.split(allInfo[1].lstrip()) #get the rank
		else:
			print("There is a problem with rank parsing:\n", allInfo, "\n",
			content)
			otherInfo = allInfo
			input("ENTER")
		print(otherInfo)
		def matchCoord(regexes, parsed, otherInfo):
				for r, myreg in enumerate(regexes):
					print(myreg)
					otherInfo = myreg.split(otherInfo)
					print(otherInfo, "HERE")
					if len(otherInfo) == 3:
						print("r =", r, otherInfo)
						parsed[r] = otherInfo[1].strip()
						otherInfo = otherInfo[2].strip()
					else:
						otherInfo = otherInfo[0]
						print(r, "=R-VALUE", )
						if r == 3: #if it's the last pass
							if len(otherInfo) > 2:
								dentry['remainder'] = otherInfo #this needs ot be expanded to do a bit of testing for being a lower level of bureaucracy on the next record		
		if len(otherInfo) == 3: #if we got a proper name split
			dentry['name'] = otherInfo[1].strip()
			otherInfo = otherInfo[2].lstrip()	
			matchCoord(regexes, parsed, otherInfo)
			indEntries.append(dentry)
		elif len(otherInfo) == 1: # we didn't sucssefully split
			#For error checking of likely names but ones outside the tolerance threshold given by the regex but I still want to parse
			potentialName = otherInfo[0].split("\n",1)[0].split(" ")	
			if len(potentialName) <= 2:
				dentry['name'] = ' '.join(potentialName)
				dentry['nameFlag'] = 1
				potentialOtherInfo =otherInfo[0].split("\n",1)
				if len(potentialOtherInfo) == 2:
					matchCoord(regexes, parsed, potentialOtherInfo[1])
			else:
				print(otherInfo, "IS AN ERROR BECAUSE THERE IS NO NAME")
				dentry['nameFlag'] = 2
				dentry['noParse'] = otherInfo #shove all the info about the record into 1 string
		print(parsed)
		dentry['title'] =parsed[0]
		dentry['email'] = parsed[1]
		dentry['phone'] = parsed[2]
		dentry['fax'] = parsed[3]
		
		entries.append(dentry)
	return(entries)


def getSubOrgData(entries):
	test = entries[:]
	for e, entry in enumerate(test):
		for i, indEntry in enumerate(entry['indEntries']):
			if i >0 and e != len(test)-1:  #and its not the last entry
				if 'remainder' in indEntry.keys():
					orgParse = recurseRemainder(indEntry['remainder'])
					if orgParse[0] != None and len(orgParse[0])>0:
						if i == len(entry['indEntries'])-1:
							#print(i, len(indEntry))
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
	org = regex.compile(r"(^[\p{Lu}](?:[[\p{Ll}\p{Lu}\-\'\(\),\s]--[\d:@\.]]+$))", regex.UNICODE + regex.V1)
	if org.match(remainder) : #if it just has org details
		orgMatch = org.match(remainder).group(1) #assign it to the org
		print(orgMatch, "ORGMATCH", nonOrg)
		return(orgMatch, nonOrg)
	elif len(remainder.rsplit("\n",1)) ==2:
		#while len(remainder.split("\n")) >1:
			#print(remainder.split("\n"), "LENGTH:", len(remainder.split("\n")),remainder.rsplit("\n")[0])
			nonOrg = nonOrg + remainder.rsplit("\n",1)[1]
			#print(nonOrg)
			#print(remainder)
			return(recurseRemainder(remainder = remainder.rsplit("\n",1)[0], nonOrg = nonOrg)) #need to return it here
			#print(nonOrg)
	else: 
		orgMatch = None
		return(orgMatch, nonOrg)
	#print("GODDAMN", orgMatch)
	

index = pd.DataFrame(columns=None)
i=1
for q, query in enumerate(anotherTest):
	for r, record in enumerate(query['indEntries']):
		myRow = record
		myRow['org'] = query['org']
		if 'ministry' in query.keys():
			myRow['ministry'] = query['ministry'] 
		print(myRow)
		row = pd.DataFrame((myRow), index = [i])
		index = index.append(row, ignore_index=True)
		print(row)
		i+=1

index.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120821.csv')




				#indEntry[i+1]['remainder']
			#have to attached it to the right entry
# mt = getData(ltest)		
# rt = getData(rtest)	

website = regex.compile(r'^www\..*\.[\p{Ll}]{2,3}', regex.UNICODE + regex.V1)

webstrings = ["www.minister.gouv.fr and some other stuff", "aaronerlic@gmail.com"]
