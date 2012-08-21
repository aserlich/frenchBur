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
		entry['indEntries'] = getData(entry['content'])
	return(entries)
		

def getData(content):
	names = regex.compile(r"""(^
								(?:
									(?:[\p{Lu}]
										(?:[\p{Ll}]{2,15}){s<=2}
										(?:[\p{Pd}][\p{Lu}][\p{Ll}]+\ |\ ){s<=1}
										(?:
											(?:
												(?:[\p{Lu}]
													(?:\'|[\p{Lu}]{2,15}){s<=1}
													(?:[\p{Pd}][\'\p{Pd}\p{Lu}]{2,15})?
												)
											)|
											(?:DE|DI|DA|DU|LE|LA)
										)
										(?:
											(?:
												(?:\ [\p{Lu}])
												(?:\'|[\p{Lu}]{2,3})
												(?:[\'\p{Pd}\p{Lu}]{0,10})
											)|
											(?:\ DE|\ DU|\ LE|\ LA)
										){0,5}
									)
									|N\.\.\.)
								)[\s,]""", regex.VERBOSE | regex.UNICODE |regex.V1)
	title = regex.compile(r"(^(?:(?:[\p{Ll}']{1,}\s)+)\n?)", regex.UNICODE)
	email = regex.compile(r'^(?:([a-zA-Z0-9+.-]+@[a-z0-9.-]+\.(?:fr|com|eu)){i<=2})', regex.UNICODE |regex.V1) #insertions to deal with blank spaces
	tel = regex.compile(r'^(?:Tél\.?\s*:\s*\+*((?:[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	fax = regex.compile(r'^(?:Fax\s*:\s*((?:\+*[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	regexes = [title, email,tel, fax]
	#print(regexes)
	#orgData = indEntries[0] 
	entries =[]
	indEntries = content.split('•') #parse by individual entry
	for e in range(1, len(indEntries)):
		dentry = {}
		allInfo = indEntries[e].split(':', 1) #split on the first semicolon before will be the rank
		print(allInfo)
		parsed =[None, None, None, None, None, None] #set up extra data spots could be used 
		if len(allInfo) ==2:
			dentry['rank'] = allInfo[0].strip()
			otherInfo = names.split(allInfo[1].lstrip()) #get the rank
		else:
			print("There is a problem with rank parsing:\n", allInfo)
			otherInfo = allInfo
			input("ENTER")
		print(otherInfo)
		if len(otherInfo) == 3: #if we got a proper name split
			dentry['name'] = otherInfo[1].strip()
			otherInfo = otherInfo[2].lstrip()
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
						dentry['remainder'] = otherInfo #this needs ot be expanded to do a bit of testing for being a lower level of bureaucracy on the next record
			indEntries.append(dentry)
		else:
			print(otherInfo, "IS AN ERROR BECAUSE THERE IS NO NAME")
			dentry['nameFlag'] = 1
			dentry['noParse'] = otherInfo #shove all the info about the record into 1 string
		print(parsed)
		dentry['parsed'] =parsed
		entries.append(dentry)
	return(entries)

mt = getData(ltest)		
rt = getData(rtest)	



