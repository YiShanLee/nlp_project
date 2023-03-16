#!/usr/bin/python
# -*- coding: utf-8 -*

"""Wikipedia Title Extractor

Uses SPARQL queries to extract all unique titles and DBPedia URLs from all DBPedia objects with the specific tags . Saves the result in the file /WikiCat/Data/titleLinks.csv

This script requires the libraries in lines 12-16 be installed within the Python
environment you are running this script in.
"""

from SPARQLWrapper import SPARQLWrapper, JSON
import math
import threading
from urllib.error import URLError
from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

# executing the SPARQL Query to get all titles and urls. 
# crawling over all results with searched tags requires threads and offsets:
# base: 50.000 multiplied by the index of the thread(so thread with index 3 starts at base 150.000)
# i: iteration of the thread. since one SPARQL call can only return up to 10.000 results, 
#	 5 calls have to be made to crawl through all 50.000 results that one thread is responsible for
def executeSparqlQuery(base, i):
	try:
		sparql.setQuery("""PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://dbpedia.org/resource/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT *
WHERE {
{?object dct:subject dbc:Medical_Terminology; rdfs:label ?label} 
UNION 
{?object dct:subject dbc:Medicine; rdfs:label ?label}
UNION
{?object dct:subject dbc:Health_care; rdfs:label ?label}
UNION
{?object dct:subject dbc:Health_sciences; rdfs:label ?label}
UNION
{?object dct:subject dbc:Diseases_and_disorders; rdfs:label ?label}
FILTER(LANG(?label) = "en")
} 
LIMIT 250""")
		sparql.setReturnFormat(JSON)
		results = sparql.query().convert()
		resultArray = []
		try:
			for result in results["results"]["bindings"]:
				if(result is None):
					continue
				else:
					resultArray.append(result["label"]["value"] + ',' + result["object"]["value"])
			if(resultArray is None):
				print('Thread: ' + self.name + '; repeat Cycle due to resultArray == None: ' + str(i))
				executeSparqlQuery(base, i)
			else:
				return resultArray
		except TypeError:
			print('Thread: ' + self.name + '; Skipped cycle due to TypeError: ' + str(i))
			executeSparqlQuery(base, i)
	except URLError:
		executeSparqlQuery(base, i)
	except EndPointInternalError:
		executeSparqlQuery(base, i)

# one thread, that downloads all assigned 50.000 results titles and urls
class myThread (threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
	def run(self):
		print("Worker No. " + self.name + " was started.")
		index = int(name)
		if(index == 0):
			base = 0
		else:
			base = 10 * index
		for i in range(1, 15):
			resultArray = []
			retries = 0
			while(retries < 10):
				resultArray = executeSparqlQuery(base, i*10)
				if(resultArray is None):
					print('Thread: ' + self.name + '; Repeat cycle due to results being empty: ' + str(i))
					retries += 1
				else:
					break
			threadLock.acquire(1)
			with open("../Data/titleLinks.csv","a", encoding='utf-8') as f:
				for x in resultArray:
					if(x is None):
						threadLock.release()
						continue
					f.write(x + "\n")
			threadLock.release()
			print('Thread: ' + self.name + '; Cycle processed: ' + str(i))

# get the number of all pages with the searched tags and save in "count"
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX : <http://dbpedia.org/resource/>
PREFIX dbpedia2: <http://dbpedia.org/property/>
PREFIX dbpedia: <http://dbpedia.org/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT count(*)
WHERE {
{?object dct:subject dbc:Medical_Terminology; rdfs:label ?label} 
UNION 
{?object dct:subject dbc:Medicine; rdfs:label ?label}
UNION
{?object dct:subject dbc:Health_care; rdfs:label ?label}
UNION
{?object dct:subject dbc:Health_sciences; rdfs:label ?label}
UNION
{?object dct:subject dbc:Diseases_and_disorders; rdfs:label ?label}
FILTER(LANG(?label) = "en")
}""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
count = int(results["results"]["bindings"][0]["callret-0"]["value"])
print('Number of objects with "searched tag: "' + str(count))

threadLock = threading.Lock()
threads = []

# use 14 threads to iterate over all pages with searched tags
threadList = [format(x,'d') for x in range(14)]
for name in threadList:
	thread = myThread(name, name)
	thread.start()
	threads.append(thread)
	
for t in threads:
    t.join()
print("Exiting Main Thread")
