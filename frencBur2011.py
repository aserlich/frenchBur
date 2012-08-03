#!/usr/bin/env python
# encoding: utf-8
"""
FrenchBur2011.py

Created by Aaron Erlich on 2012-08-01.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import regex
import pandas as pd
import numpy
import scipy


burs = pd.DataFrame(columns=['name', 'surname', 'rank', 'title' ], dtype = object) # , name = "frenchbur")
burs = burs.reindex([1])
burs.dtypes
burs.ix[:1] = "fuck"

# 1) create a two dimensial array where each name gets an entry
# 2) go through the lines until I find a title
# 3) if there is text after the title, then that's the name but run checks
#4 4) if there is no text, take the next line and evaluate as the name -- put it in the db
	#if it is "N...", then make it an NA
# 5) After name is entered, evaluate folloing lines with regular expressions for all of the following potential info
#		1)email
#		2)tel
#		3)fax		
#		4)address
#		5) keep track of how many lines down this goes
# 6) The next line will be a title of a bureacratic level associated with the next name
#	Which needs to to stored to put into the next persons entry

os.chdir('/Volumes/Optibay-1TB/FrenchBur/2011/output')



jobs = []
fh = open('/Volumes/Optibay-1TB/FrenchBur/2011/gouv2011.003.txt')
x = fh.readlines()
for i in range(0, len(x)):
	m = regex.search('•\s*(\X+)\s*:\s*', x[i])
	if m != None:
		jobs.append(m.group(1).strip())
		print(x[i])

locs =[]
fh = open('/Volumes/Optibay-1TB/FrenchBur/2011/gouv2011.003.txt')
x = fh.readlines()
for i in range(0, len(x)):
	print(x[i])
	m = regex.search(r'•\s*(.*)\s*:\s*', x[i])
	if m != None:
		locs.append(i)
		print(m.group(1))


#flag for determing unicode word boundaries
flags=regex.WORD

jobsout = open('jobs.csv','w')

myfile = open('jobs.csv', 'wb')
jobsout = csv.writer(myfile, quoting=csv.QUOTE_ALL)
jobsout.writerows(jobs)

myfile = open('jobs.csv', 'wb')

email = regex.compile(r'([a-zA-Z0-9+.-]+@[a-z0-9.-]+.fr)', flag=regex.UNICODE)
tel = regex.compile(r'Tél\.\s*:\s*\+*((?:[0-9]\s?){10,14})', flag=regex.UNICODE)
fax = regex.compile(r'Fax\.\s*:\s*\+*((?:[0-9]\s?){10,14})', flag=regex.UNICODE)

storage = []
garbage = []	
fh = open('/Volumes/Optibay-1TB/FrenchBur/2011/gouv2011.003.txt')
x = fh.readlines()
for i in locs:
	keys = ['loc','name','rank','email','tel','fax']
	D= {key: None for key in keys}
	D['loc'] = i
	m = regex.split(r'•\s*(.*?):\s*',x[i])
	if len(m[2].strip()) == 0:
		D['rank'] = m[1].strip()
		#print(D['rank'])
		ecount = 0 
		tcount = 0
		fcount = 0
		em = regex.search(email, x[i+1])
		if  em != None:
			D['email'] = em.group(1).strip()
			#print(D['email'])
			ecount = 1
		te = regex.search(tel, x[i+1])
		if te != None:
			D['tel'] = te.group(1).strip()
			tcount = 1
		fa = regex.search(fax,  x[i+1])	
		if fa != None:
			D['fax'] = fa.group(1).strip()
			fcount = 1
		if ecount == 1:
			nm = regex.split(email, x[i+1])
			D['name'] = nm[0].strip()
		elif tcount	== 1:
			nm = regex.split(tel, x[i+1])
			D['name'] = nm[0].strip()
		elif fcount	== 1:
			nm = regex.split(tel, x[i+1])
			D['name'] = nm[0].strip()
		else:
			D['name'] = x[i+1].strip()
			#print(D['name'])
	else: #this needs to be fixed for checking all the stuff on the same line
		em = regex.search(email, x[i])
		if  em != None:
			D['email'] = em.group(1).strip()
			print(D['email'])
			ecount = 1
		D['name'] = m[2].strip()
		D['rank'] = m[1].strip()
	storage.append(D)

res = pd.DataFrame(columns=keys)
for q in range(0, len(storage)):
	row = pd.DataFrame((storage[q]), index = [q])
	res = res.append(row, ignore_index=True)
	
DataFrame.to_csv

res.to_csv('/Volumes/Optibay-1TB/FrenchBur/2011/output/frenchBur20120802.csv')
		
fh = open('/Volumes/Optibay-1TB/FrenchBur/2011/gouv2011.003.txt')
for line in fh.readlines():
	line

	
	#m = re.search('(?<=•)\w+', line)
	print(m(0), end = "")

for line in fh.readlines():
	#print(line.split("•")[1], end = "")
	print(re.findall( '•(.*):', line))
	re.findall( '•(.*):', line)


t = re.split(r'^•(.*):', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')


#compiles a regular expression so it doesn't need to be re-evaluated
tMat = regex.compile(r'•\s*(\X+)\s*:\s*')
t = regex.split(tMat, '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')

#once you have the name - this gets the fist name
y = str(x).split(r" ")[0]

#all foreign phone numbers have a +

#all domestic addresses have 

#this works but takes foreer
t = regex.split(r'•\s*(\X+)\s*:\s*', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')
#this works is less accurate but may be good enough
bool(regex.match(r'•\s*(.+)\s*:\s*',  '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI'))

if regex.match(r'•\s*(.+)\s*:\s*',  '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')
	print("fuck")

t = regex.split(r'^•\s*(\X+)\s*:', '•	Directrice adjointe du cabinet :     ')
t = regex.split(r'^•\s*(\b\w*\p{script=Latin}+\b)\s*:\s*', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')
t = regex.split(r'^•\s*(\b\w*\X+\b)\s*:\s*', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')
t = regex.split(r'^•\s*(\w*|\s):\s*', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')

t = regex.split(r'^•\s*(\b[\p{Ll}\p{Lo}]]\b)\s*:\s*', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI')

t = regex.split(r'^•\s*(\b[\p{Ll}\p{Lo}]\b+)\s*:', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI    ')

t = regex.split(r'^(\b\w*[\p{Ll}\p{Lo}]\b+)', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI    ')

t = regex.split(r'^(\b\w*[\p{Ll}\p{Lo}]\b+)', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI    ')

t = regex.split(r'^(\b\w*[\p{Ll}\p{Lo}]\b+)', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI    ')


t = regex.findall(r'Tél\.\s*:\s*([0-9]\s?{10,14})', '44036 Nantes Cedex 1 Tél. : 02 51 77 24 59 Fax : 02 51 77 24 60', flag=regex.UNICODE)


#get telephone number
t = regex.findall(r'Tél\.\s*:\s*\+*((?:[0-9]\s?){10,14})', '44036 Nantes Cedex 1 Tél. : 02 51 77 24 59 Fax : 02 51 77 24 60', flag=regex.UNICODE)

#fax number
t = regex.findall(r'Fax\.\s*:\s*\+*((?:[0-9]\s?){10,14})', '44036 Nantes Cedex 1 Tél. : 02 51 77 24 59 Fax : 02 51 77 24 60', flag=regex.UNICODE)


#email
t = regex.split(r'([a-z+.-]+@[a-z+.-]+.fr)', 'administrateur civil guillaume.dechanlaire@ville.gouv.fr Tél. : 01 49 17 45 73')


t = regex.split(r'^•(\b\w*\b)\s*:\s*', '•	Directrice adjointe du cabinet : Marie-Anne BARBAT-LAYANI', flag=regex.UNICODE)


nameMatch = re.compile('•'(\p{Latin}*))	
m =re.search(nameMatch, "•	Secrétaire général :")

m = regex.search(r'•\s*(\p{Latin}+\v)\s*:\s*','•Secrétaire général :')
m = regex.search('•\s*(\X+)\s*:\s*','•Secrétaire général :')


m = re.search( r'•(.*):','•Secrétaire général :')

m = re.findall( r'•(.*):','•Secrétaire général :')

#WORKS
re.findall( '•(.*):','•Secrétaire général :')
m = re.search( r'•(.*):','•Secrétaire général :')
#returns only the matched part of the regular expresion
m.group(1)

re.findall( '•(.\p{Latin}*.*):','•Secrétaire général :')

#matches any Latin Character
\p{Latin}

•

columns 


def main():
	pass


if __name__ == '__main__':
	main()

