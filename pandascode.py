res = DataFrame(columns=('lib', 'qty1', 'qty2'))
row = pd.pandas.DataFrame([dict(lib='hello', qty1=4.0, qty2=100.0), ])

regex.split('•\s*(.+)\s*:\s*','•	Directeur du cabinet : jean-Paul FAUGÈRE')

m = regex.split(r'•\s*(.*?):\s*',x[31330])

# hello.py
def hello():
    print "Hello World!"
    return

# map.py
# We can use append here
def map( fun, list ):
    nlist = []
    for item in list:
        nlist.append( fun( item ) )
    return nlist
# But here we have to use concatenation, or the + operator for lists.
def rmap ( fun, list ):
    if list == []:
        return []
    else:
        return [fun( list[0] )] + rmap( fun, list[1:] )

# Make a sample test function
def increment(x):
    return x+1

map( increment, [1,2,3,4,5] )

regex.findall(r'([\p{Lu}]{2,20}\-?\'?[\p{Lu}]{0,20})', "john smit", flag=regex.UNICODE)
regex.findall(r'([\p{Lu}]{2,20}\-?\'?[\p{Lu}]{0,20})', "Emmanuelle WARGON conseillère référendaire à la Cour des comptes", flag=regex.UNICODE)

#test page numbers
pnO = regex.compile(r'#\s?([1-9][0-9]{0,2})', flag = regex.UNICODE)
pnE = regex.compile(r'^\s?([1-9][0-9]{0,2})\s?#', flag = regex.UNICODE)
regex.findall(pnO, '412 # Répertoire de l\'administration française 2011')
regex.findall(pnO, 'Répertoire de l\'administration française 2011 #413')
regex.findall(pnE, 'Répertoire de l\'administration française 2011 #413')
regex.findall(pnE, 'Répertoire de l\'administration française 2011 #413')
regex.findall(pnE, 'Répertoire de l\'administration française 2011 # 413')
regex.findall(pnO, 'Répertoire de l\'administration française 2011 # 413')
regex.findall(pnE, '408 # Répertoire de l\'administration française 2011')
regex.findall(pnE, '408# Répertoire de l\'administration française 2011')


ac =regex.compile(r'\.+([1-9][0-9]{0,2})\n', flag = regex.UNICODE)
regex.findall(ac, '...645\n')

f = codecs.open('/Volumes/Optibay-1TB/FrenchBur/2011/rawText/indices2011.007_indexadministrationcentrales.txtCLEANED.txt','w+')
for i in range(0, len(x)):
	if i not in locs:
		f.write(x[i].strip())
#f.seek(0)
xmod = f.readlines()


ac = regex.compile(r'\.*([1-9][0-9]{2}|[7-9][0-9])\n', flag=regex.UNICODE)
ac2 = regex.compile(r'\.*([1-9][0-9]{2}||[7-9][0-9])', flag=regex.UNICODE)
regex.split(ac2, 'Secrétariat général de la présidence française du G20 et du G8')

x = '•	inspecteur hygiène et sécurité'
y = x.find('•')
x = x.find(':')
try:
	 x.index(':')
except ValueError:
	print("hello")



ntest = ['Michèle DUBROCARD magistrate', ' Marie-Sara durur Marie-Sara.Durur@justice.gouv.fr Tél. : 01 70 22 41 71', 
'Jean-Pierre KELCHE, général d\'armée','ÉriC LE CLERCQ DE LANNOY', 'ÉriC LE CLERCQ DE LANNOY, fucker',
 'Éric LE CLERCQ DE LANNOY shlaphead', "john smith proctologist", 'John smith Proctolog', 'john smith, proctolog', "N...", "GHESTEM", "Bill linebreaker,"
"his honorable Baron VAN BULL and her hc Marie-Eunice DELAGARDE", "John DU LA FEH", "Creme DE CREME MADAME", "Joe THE HIP HOP KING"]

for i in range(0, len(ntest)):
	checkName(ntest[i], {}, " ")

for i in range(0, len(ntest)):
	emtefa(ntest[i], {}, "specialist of a random sort" )


for i in range(0, len(ntest)):
	f = regex.findall(r'([\p{Lu}]+\-?\'?[\p{Lu}])',ntest[i], flag=regex.UNICODE)
	index = ntest[i].find(f[-1])
	end = index +len(f[-1]) + 1
	part1 = ntest[i][0:end]
	part2 = ntest[i][end:len(ntest[i])]
	print(part1)
	print(part2)
	
##More regex learning
#any word that starts with q not followed by a U
#Pd is any dash and this demonstrate regex works with unicode characters and the \p suite for unicode
regex.findall(r'q[^u][\w\p{pd}]*',"qwerty quilty quacké qi qosheré qoc-henü")
re.findall(r'q[^u][\w\p{pd}]*',"qwerty quilty quacké qi qosheré qoc-henü")

names = regex.compile(r"""[\p{Lu}][\p{Ll}]{2,15}(?:[\p{Pd}][\p{Lu}][\p{Ll}]+\ |\ )
					(?:(?:[\p{Lu}])(?:'|[\p{Lu}]{2,3})(?:['\p{Pd}\p{Lu}]{0,10})|(?:DE|DU|LE|LA))
					(?:(?:(?:\ [\p{Lu}])(?:'|[\p{Lu}]{2,3})(?:['\p{Pd}\p{Lu}]{0,10}))|(?:\ DE|\ DU|\ LE|\ LA)){0,5}""", regex.VERBOSE | regex.UNICODE)

for i in range(0, len(ntest)):
	print(regex.findall(names,ntest[i]))
	
	
print(item['pageNum'] for item in entDict[0])


x = regex.search(r"(Agence de gestion du réseau international des finances RESINTER  e{<=3})", mys, regex.V1, regex.UNICODE, regex.IGNORECASE) 

pattern = "(" +regex.escape("Agence de gestion du réseau international des finances RESINTER", regex.UNICODE |regex.V1 | regex.IGNORECASE) +")"+ '{e<=10}' 
x = regex.findall(pattern, "Agence de gestion du réseau international des finances RESINTER ", regex.V1 | regex.UNICODE | regex.IGNORECASE)

mys =("•	Chargé de communication extérieure et de l'accueil des tournages : André ETANCELIN andre.etancelin@apie.gouv.fr Tél. \
: 01 53 44 27 37 Fax : 01 53 44 27 39 Agence de gestion du réseau international des finances RESINTER www.minefe.gouv.fr •")


title = regex.compile(r'([[\p{Ll}\p{Lu}\s]--[\.]]+).*', regex.UNICODE | regex.VERSION1)
stuff= ("\tMinistère de l'Économie, des Finances et de l'industrie\t...............................................270 \
Ministre chargé de l'industrie, de l'Énergie et de l'Économie numérique\
...............................................   ........................................271 \
Secrétaire d'État chargé du Commerce extérieur \
.......................................................................................................\
...............................................................271 ")
getrec = regex.compile(r'([[\D]--[0-9]]+[1-9][0-9]{1,2}\s)', regex.UNICODE | regex.VERSION1)
#str_list = filter(None, str_list)
regex.split(num, stuff)
regex.findall(title, "asdfsdf...")


org = "Direction générale pour l'enseignement supérieur et l'insertion professionnelle (DGESIP)"
asRE1 = regex.escape(org.strip().upper(), regex.UNICODE)
pattern1 = "\\s(?:(" + asRE1 +")"+ '{s<=3, i<=1, d<=1})' 
myreg1 = regex.compile(pattern1,  regex.VERSION1 + regex.FULLCASE) #if version is already turned on do not term in in match

myString = "•\tDélégué général : Bernard BENHAMOU •\tSecrétaire général : Pierre PEREZ pierre.perrez@education.gouv.fr Tél. : 01 55 55 99 69 DIRECTION GÉNÉRALE POUR L'ENSEIGNEMENT SUPÉRIEUR ET L'INSERTION PROFESSIONNELLE (DGESIP) Tél. : 01 55 55 63 00 Fax : 01 55 55 60 03 •\tDirecteur: Patrick HETZEL professeur des universités "

myreg1.findall(myString)


rtest = beEntriesT2[200]['content']
ltest = beEntriesT2[400]['content']


title = regex.compile(r"(^(?:(?:[\p{Ll}']{1,}\s)+)\n?)", regex.UNICODE)

# title = regex.compile (r"""(^(?:(?:[\p{Ll}']{1,}\s)+\n)
# 						(?:\s?\p{Lu}[\p{Ll}'] | .*?@))
# 						)""", regex.UNICODE | regex.V1 |regex.VERBOSE)

testStrings = ["ingénieur général de l'armement Organismes relevant du chef d'état-major des armées\n", 
				"ingénieur général de l'armement\n Organismes relevant du chef d'état-major des armées\n"]

nameStrings = ['Evelyne LIDOVE-THOMMERET, docteur evelyne.lidove-thommeret@pm.gouv.fr\n ', 'Sophie DUHAMEL-LACOSTE\n sophie.duhamel-lacoste@pm.gouv.fr\n',
				'Sophie DUHAMEL-LACOSTE sophie.duhamel-lacoste@pm.gouv.fr\n', 'Florian LEZEC, rank: Chef de la mission', 'Florian L\'EZEC shithad',
				'madame LE COW big udders', "EriC BOUSSION DE BOUBOIR, bunny"
				]

names = regex.compile(r"""(^
							(?:
								(?:[\p{Lu}]
									(?:[\p{Ll}]{2,15}){s<=2}
									(?:[\p{Pd}][\p{Lu}][\p{Ll}]+\ |\ )
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

for i in range(0, len(nameStrings)):
	names.split(nameStrings[i])
	names.findall(nameStrings[i])

for i in range(0, len(testStrings)):
	title.split(testStrings[i])
	title.findall(testStrings[i])



#evetually should work for multiple phone numbers	

def myTokens(tokenized, entryName, isCoord, dentry):
	if len(tokenized) == 3:
		print("Yay")
		dentry[entryName] = tokenized[1]
		if len(tokenized[0]) > 2:
			dentry['title'] = tokenized[0]
		isCoord += 1

def matchEmail(string):
	email = regex.compile(r'(?:([a-zA-Z0-9+.-]+@[a-z0-9.-]+\.(?:fr|com|eu)){i<=2})', regex.UNICODE |regex.V1)
	if email.search(string):
		tokenized = email.split(string)
	elif not email.search(string):
		tokenized = string
	return(tokenized)
	

def matchTel(string):
	tel = regex.compile(r'(?:Tél\.\s*:\s*\+*((?:[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	if tel.search(string):
		tokenized = tel.split(string,1)
	elif not tel.search(string):
		tokenized = string
	return(tokenized)

def matchFax(string):
	fax = regex.compile(r'(?:Fax\.\s*:\s*((?:\+*[0-9]\s?){10,14}){e<=1})', regex.UNICODE | regex.V1)
	if fax.search(string):
		tokenized = fax.split(string,1)
	elif not fax.search(string):
		tokenized = string
	return(tokenized)



	

indEntries = rtest.split('•')
indEntries[1].split(':', 1)
		
		