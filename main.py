"""Helpful docs:
https://nedbatchelder.com/text/unipain.html
https://stackoverflow.com/questions/39229439/encoding-error-when-reading-url-with-urllib
"""
import requests
import json

start_keyword = input("Type keyword to start with -> ")
print(start_keyword)

def getSugsFromFile(url, word):
	
	query = url.format(word)
	
	try:
		data = None
		data = requests.get(query).content.decode('utf-8','ignore')
		data = json.loads(data)
	
		if url == 'https://api.qwant.com/api/suggest/?q={}':
			# DATA STRUCTURE
			"""
			'{
				"status":"success",
				"data":{
					"items":[{"value":"footmercato","suggestType":7},{"value":"foot01","suggestType":7},{"value":"foot","suggestType":7},{"value":"football365","suggestType":7},{"value":"footao","suggestType":7},{"value":"footasse","suggestType":12},{"value":"football","suggestType":3}],
					"special":[]
				}
			}'
			"""
			for item in data['data']['items']:
				yield item['value']

		elif url == 'https://duckduckgo.com/ac/?q={}':
			"""
			[ {'phrase': 'foot locker'},{'phrase': 'foodspring'},{'phrase': 'football tv hd'} ]
			"""
			for item in data:
				yield item['phrase']

		elif url == 'https://suggestqueries.google.com/complete/search?client=firefox&q={}' or url == 'http://completion.amazon.com/search/complete?search-alias=aps&client=amazon-search-ui&mkt=1&q={}':
			""" GOOGLE DATA STRUCTURE
				[
					'foo',
					['foot locker', 'foodspring', 'football tv hd', 'football', 'footloose', 'foodscovery', 'foo fighters', 'football24', 'foodracers', 'foodracers milano'],
					[],
					{
						'google:suggestsubtypes': [ [433], [433], [433], [433], [433, 131], [], [433], [433, 131], [433, 457], [402] ]
					}
				]
			"""
			""" AMAZON DATA STRUCTURE
				[
					'foo',
					['whole foods', 'food', 'food scale', 'cat food', 'dog food storage container', 'foot peel mask', 'food storage containers', 'foot scrubber', 'foot spa', 'keto food'],
					[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
					[],
					'3QSAOI3091EZR'
				]
			"""

			for item in data[1]:
				yield item


	except requests.exceptions.ConnectionError as e:
		print( "[!] Connection Error\n---details---\n{}\n---\n".format(e) )


api_urls = [ 
				'https://api.qwant.com/api/suggest/?q={}',
				'https://duckduckgo.com/ac/?q={}',
				'https://suggestqueries.google.com/complete/search?client=firefox&q={}',
				'http://completion.amazon.com/search/complete?search-alias=aps&client=amazon-search-ui&mkt=1&q={}',				
			]

results = set()
for api in api_urls:
	print("[*] Using API: ", api)
	for result in getSugsFromFile(api, start_keyword):
		results.add(result)
		for res in getSugsFromFile(api, result):
			results.add(res)

#print(results,"\n")


import string
import urllib
alphabet = string.ascii_lowercase[:26] #'abcdefghijklmnopqrstuvwxyz'

print("\nALPHABETIC ADDITIVES\n")

for api in api_urls:
	print("[*] Using API: ", api)
	for i in range(0, len(alphabet) ):
		print("[*] Letter: ", alphabet[i].upper() )
		keyword = urllib.parse.quote_plus(start_keyword+" "+alphabet[i])
		for res in getSugsFromFile( api, keyword ):
			results.add( res )

print("\n",results,"\n")
