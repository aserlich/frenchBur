##Doesn't work but kept for completeness sake

soup = BeautifulSoup(open("/Volumes/Optibay-1TB/FrenchBur/2011/rawText/gouv2011.003.htm"))

namesetal = soup.findAll("span", {"class": "font8"}) #finds everything between the beginning and end of a span with class font8

f8 = []
for i in (range(0, len(namesetal))):
	f8.append(namesetal[i].contents) #gets the text contents


<p><span class="font8">N...</span></p>

