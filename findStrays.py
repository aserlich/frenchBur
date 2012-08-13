#!/usr/bin/env python
# encoding: utf-8
"""
findStrays.py

Created by Aaron Erlich on 2012-08-10.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

def findStrays(prevLines, fileName):
	"""
	Iterate through the file to find all names that match the regexp criteria for names but are not already in the database of names
	"""
	namedb =[]
	names = regex.compile(r"""[\p{Lu}][\p{Ll}]{2,15}(?:[\p{Pd}][\p{Lu}][\p{Ll}]+\ |\ )
					(?:(?:[\p{Lu}])(?:'|[\p{Lu}]{2,3})(?:['\p{Pd}\p{Lu}]{0,10})|(?:DE|DI|DA|DU|LE|LA))
					(?:(?:(?:\ [\p{Lu}])(?:'|[\p{Lu}]{2,3})(?:['\p{Pd}\p{Lu}]{0,10}))|(?:\ DE|\ DU|\ LE|\ LA)){0,5}""", regex.VERBOSE | regex.UNICODE)
	fh = open(fileName)
	#fh.seek(0)
	x = fh.readlines()
	fh.close()
	print(len(x))
	input(" ")
	nonNames = 	["Télédoc","Télécopie","Site","Contact", "Groupe", 
				"France","Cellule","Délégation","Mission","Département","Centre", "Télécom",
				"Fonds", "Iles","Valletta","Bâtiment","Secteur"] #these items are followed by captialized patters so they look like names (e.g, Fonds MARCH)
	for i in range(0, len(x)): #go trhough the file
		#print(i)
		if i not in prevLines: #if the line has not previously contained a name
			f = regex.findall(names, x[i])
			if len(f) >0:
				for ents in range(0,len(f)):
					#print(ents)
					if f[ents].split(" ")[0] not in nonNames: #if the first word is not in nonNames
						entry ={}
						name =' '.join(["name",str(ents+1)])
						entry[name] = f[ents]
						entry['loc'] = i
						entry['strayFlag'] = 1 
						namedb.append(entry)
				#print(f)
				#input("")
	return(namedb)

