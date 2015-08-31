from os import listdir					#for getting the list of all files inside a directory
from os.path import isfile,join			#for same as above
from whoosh.index import create_in		#for creating schema
from whoosh.fields import *				#for defining fields in schema
from BeautifulSoup import BeautifulSoup	#for extracting only text
from whoosh.writing import AsyncWriter	
import time
import sys
from whoosh.qparser import QueryParser

#declare variables
file_names = []		#stores all the file names

def get_allfiles(files_path):
	for x in listdir(files_path):
		if (not x.endswith('~')) and isfile(files_path+"/"+x):
			file_names.append(files_path+"/"+x)

def create_schema():
	global schema,ix,writer
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT, time=DATETIME(stored=True))
	ix = create_in("Datasets", schema)
	writer = ix.writer()

def index_allfiles():
	for x in file_names:
		file_data=""
		with open(x) as file:
			file_data = file.read()
			file.close()
		try:
			soup = BeautifulSoup(file_data)
		except UnicodeEncodeError:
			print "Soup error: "+x
		except TypeError:
			soup = BeautifulSoup(file_data.decode('utf-8','ignore'))
		if soup.title is None:
			page_title = " "
		else:
			page_title = soup.title.string
		for script in soup(["script", "style"]):
			script.extract()
		data = soup.getText(separator=u' ')
		try:
			writer.add_document(title=unicode(page_title), path=unicode(x), content=unicode(data))
		except UnicodeDecodeError:
			print "Error in " + x
		except UnicodeEncodeError:
			print "Error in " + x
	writer.commit()
	
def main():
	for x in range(27,29): get_allfiles("Datasets/"+str(x))
	create_schema()
	start = time.time()
	index_allfiles()
	end = time.time()
	print "Time taken to index data: "
	print (end-start)
	with ix.searcher() as searcher:
		query = QueryParser("content", ix.schema).parse("cars")
		results = searcher.search(query)
		print results
if __name__== "__main__":        
    main()
