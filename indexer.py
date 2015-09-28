import os                  #for getting the list of all files inside a directory
from os.path import isfile,join         #for same as above
from whoosh.index import create_in      #for creating schema
from whoosh.fields import *             #for defining fields in schema
from BeautifulSoup import BeautifulSoup, Comment #for extracting only text
from whoosh.qparser import QueryParser
import time
from whoosh.analysis import *

def create_schema():
    global schema_stsw,schema_sw,schema_st,schema,ix,writer_stsw,writer_st,writer_sw,writer
    schema_stsw = Schema(path=ID(stored=True,analyzer=StemmingAnalyzer()),title=TEXT(stored=True,analyzer=StemmingAnalyzer()),content=TEXT(stored=True,analyzer=StemmingAnalyzer()))
    schema_st   = Schema(path=ID(stored=True,analyzer=StemmingAnalyzer(stoplist=None)),title=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=None)),content=TEXT(stored=True,analyzer=StemmingAnalyzer(stoplist=None)))
    schema_sw   = Schema(path=ID(stored=True,analyzer=StandardAnalyzer()),title=TEXT(stored=True,analyzer=StandardAnalyzer()),content=TEXT(stored=True,analyzer=StandardAnalyzer()))
    schema      = Schema(path=ID(stored=True,analyzer=SimpleAnalyzer()),title=TEXT(stored=True,analyzer=SimpleAnalyzer()),content=TEXT(stored=True,analyzer=SimpleAnalyzer()))

    ix          = create_in("Indexed/Index_stsw", schema_stsw)
    writer_stsw = ix.writer()
    ix          = create_in("Indexed/Index_st", schema_st)
    writer_st   = ix.writer()
    ix          = create_in("Indexed/Index_sw", schema_sw)
    writer_sw   = ix.writer()
    ix          = create_in("Indexed/Index", schema)
    writer      = ix.writer()

def index_allfiles(mainDirectory):
    for root, subFolders, files in os.walk(mainDirectory):
        for x in files:
            if not x.endswith('~'):
                fullpath = os.path.join(root, x) 
                with open(fullpath,'r') as f:
                    file_data = f.read()
                    
                try:
                    soup = BeautifulSoup(file_data)
                except UnicodeEncodeError:
                    print "Soup error: "+x
                except TypeError:
                    file_data = file_data.decode('utf-8','ignore')
                if soup.title is None:
                    page_title = "Title Undefined"
                else:
                    page_title = soup.title.string
                for script in soup(["script", "style"]):
                    script.extract()
                comments = soup.findAll(text=lambda text:isinstance(text, Comment))
                [comment.extract() for comment in comments]
                data = soup.getText(separator=u' ')
                data = data.replace("&nbsp"," ")
                try:
                    writer_stsw.add_document(path=unicode(fullpath),title=unicode(page_title),content=unicode(data))
                    writer_st.add_document(path=unicode(fullpath),title=unicode(page_title),content=unicode(data))
                    writer_sw.add_document(path=unicode(fullpath),title=unicode(page_title),content=unicode(data))
                    writer.add_document(path=unicode(fullpath),title=unicode(page_title),content=unicode(data))
                except UnicodeDecodeError:
                    print "Error in " + x
                except UnicodeEncodeError:
                    print "Error in " + x
            
    writer_stsw.commit()
    writer_st.commit()
    writer_sw.commit()
    writer.commit()
    
def main():
    create_schema()
    start = time.time()
    index_allfiles("Datasets")
    end = time.time()
    print "Time taken to index data: "
    print (end-start)

main()
