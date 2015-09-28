#!/usr/bin/python
import cgitb
from whoosh.qparser import QueryParser
from os import listdir					#for getting the list of all files inside a directory
from os.path import isfile,join			#for same as above
from whoosh.index import create_in,exists_in,open_dir		#for creating schema
from whoosh.fields import *				#for defining fields in schema
from whoosh import scoring
import cgi
from BeautifulSoup import BeautifulSoup	#for extracting only text
import sys
import os
from whoosh import qparser
from whoosh import analysis, fields, formats, query, highlight
import time
def searchpage():
	global results, time_tf
	print ('''
	<!DOCTYPE HTML>
	<html>
		<head>
		    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			<link href="Bootstrap/css/bootstrap.css" rel="stylesheet">
			<link href="Bootstrap/css/bootstrap.min.css" rel="stylesheet">
			<link href="Bootstrap/css/bootstrap-theme.css" rel="stylesheet">
			<link href="Bootstrap/css/bootstrap-theme.min.css" rel="stylesheet">
			
			<link href="BootstrapSwitch/css/main.css" rel="stylesheet">
		    <link href="BootstrapSwitch/css/highlight.css" rel="stylesheet">
		    <link href="BootstrapSwitch/dist/css/bootstrap3/bootstrap-switch.css" rel="stylesheet">
		    <link href="BootstrapSwitch/css/other.css" rel="stylesheet">
		    <script src="BootstrapSwitch/js/jquery.min.js"></script>
		    <script src="BootstrapSwitch/dist/js/bootstrap-switch.js"></script>
		    <script src="Bootstrap/js/bootstrap.min.js"></script>
                    <script src="Graph/js/highcharts.js"></script>
                    <script src="Graph/js/modules/exporting.js"></script>
		    <script>
		    $(function(argument) {
		      $('[type="checkbox"]').bootstrapSwitch();
		    })
			</script>
			<title>InfoZeal</title>
		</head>
		<body>''')
	print ('''
			<div class="panel panel-default">
				<div class="panel-heading">
					<form class="form-inline" id="myForm" role="form" action="#" method="post">
					<div class="row">
						<div class="col-lg-6">
							<div class="input-group">
								 <div class="row">
									<div class="col-lg-2">
										<img src="images/logo.jpg" class="image-logo"/>
									</div>	
						
									<div class="col-lg-6">
										<div class="input-group">
                                                                                        <input type="hidden" name="hiddenOption" id="hiddenOption">
                                                                                        <input type="hidden" name="relTf" id="relTf" value=''')
	print str(relTf)
	print                                                                                        ('''>
                                                                                        <input type="hidden" name="relTfidf" id="relTfidf" value=''')
	print str(relTfidf)
	print                                                                                        ('''>
                                                                                        <input type="hidden" name="relBm" id="relBm" value=''')
	print str(relBm)
	print                                                                                        ('''>
                                                                                        <input type="hidden" name="numQ" id="numQ" value=''')
	print str(count)
	print 																				('''>
											<input type="text" class="search_box" id="query" name="query" value=
		  ''')
	print ("'" + query +"'")
	print ('''								>
											<span class="input-group-btn">
												<input type="submit" id="submitButton" class="btn btn-default">Search
											</span>
										</div>
									</div>
								</div>
								
							</div>
						</div>
						&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
						
						Stemming&nbsp&nbsp&nbsp<input class="form-control" name="stem" id="stem" value="stemming" type="checkbox">
						&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
						Stop Word&nbsp&nbsp&nbsp<input class="form-control" type="checkbox" name="stop" value="stopping" id="stop">
						&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                                                &nbsp&nbsp&nbsp 
                                        <div class="btn-group">
                                            <button type="button" class="btn btn-primary">Options</button>
                                                    <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                        <span class="caret"></span>
                                                            <span class="sr-only">Toggle Dropdown</span>
                                            </button>
                                                            <ul class="dropdown-menu">
                                                            	<li><a onclick="hitOption(0)">MAP</a></li>
                                                                <li><a onclick="hitOption(1)">NDCG</a></li>
                                                                <li><a onclick="hitOption(2)">Search Engine</a></li>
                                                            </ul>
                                            </div>
						
					</div>
				</div>
				</form>
				<div class="result-panel-body-main">
                                    <div class="row">
                                        <div class="col-lg-7">
                                            <ul class="nav nav-tabs">
                                              <li class="active"><a data-toggle="tab" href="#tf">Term Frequency</a></li>
                                              <li ><a data-toggle="tab" href="#tfidf">Invert Document Term Frequency</a></li>
                                              <li ><a data-toggle="tab" href="#bm25">Best Match 25</a></li>
                                            </ul>
                                        </div>
                                        <div class="col-lg-2">
                                        <span class="input-group-btn">
                                                <button class="btn btn-primary" id="nQ" type="button" onclick="nextQuery()">Next Query</button>
                                        			
                                                <button class="btn btn-success" id="cal" type="button" onclick="calculate()">Calculate MAP</button>
                                        </span>
                                        </div>
                                        
                                    </div>
					<div class="tab-content">
						<div id="tf" class="tab-pane fade in active">
							<h6>&nbsp&nbsp
		  ''')
	
	if int(count)==10000:
		print ('''<div class="panel panel-default">
		  <div class="panel-heading">
			<h3 class="panel-title">Mean Average Precision TF </h3>
		  </div>
		  <div class="analytics-panel-body">''')
		print relTf
			
		print('''
		</div>''')
	else:
		if time_tf is not None:
			print str(len(results_tf)) + " results (" + str(time_tf) +" seconds)"
			print ('''				</h6>
								<p>
			  ''')
		for x in results_tf:
			print ('''
								<div class="result-panel-heading">
									<div class="result_title">
										<h6 class="result-title-heading">
											<a href="''')
			print x['path'].encode('utf-8')
			print ('''"							>
				  ''')
			print x['title'].encode('utf-8')
			print ('''							</a>
			                                                                       <input id="switch-size" value="rel" class="tfRel" type="checkbox" data-size="mini">
			                                                                        </h6>
											<h6 class="result-title-path">	
				  ''')
			print x['path'].encode('utf-8')

			print ('''						</h6>
										</div>
										<div class="result-panel-body">
				  ''')							
			print x.highlights("content",top=20).encode('utf-8')
			print ('''					</div>
									</div>
				''')
	print ('''				</p>
						</div>
					<div id="tfidf" class="tab-pane fade">
					<h6>&nbsp&nbsp''')
	
	if int(count)==10000:
		print ('''<div class="panel panel-default">
		  <div class="panel-heading">
			<h3 class="panel-title">Mean Average Precision TFIDF </h3>
		  </div>
		  <div class="analytics-panel-body">''')
		print relTfidf
			
		print('''
		</div>''')
	else:
		if time_tfidf is not None:
			print str(len(results_tfidf)) + " results (" + str(time_tfidf) +" Seconds)"
			print ('''				</h6>
								<p>
			  ''')
		for x in results_tfidf:
			print ('''
								<div class="result-panel-heading">
									<div class="result_title">
										<h6 class="result-title-heading">
											<a href="''')
			print x['path'].encode('utf-8')
			print ('''"							>
				  ''')
			print x['title'].encode('utf-8')
			print ('''							</a>
			                                                                        <input id="switch-size" value="rel" class="tfidfRel" type="checkbox" data-size="mini">
											</h6>
											<h6 class="result-title-path">	
				  ''')
			print x['path'].encode('utf-8')

			print ('''						</h6>
										</div>
										<div class="result-panel-body">
				  ''')							
			print x.highlights("content",top=20).encode('utf-8')
			print ('''					</div>
									</div>
					''')
	print ('''				</p>
						</div>
						<div id="bm25" class="tab-pane fade">
							<h6>&nbsp&nbsp''')
	
	if int(count)==10000:
		print ('''<div class="panel panel-default">
		  <div class="panel-heading">
			<h3 class="panel-title">Mean Average Precision BM25 </h3>
		  </div>
		  <div class="analytics-panel-body">''')
		print relBm
			
		print('''
		</div>''')
	else:
		if time_bm25 is not None:
			print str(len(results_bm25)) + " results (" + str(time_bm25) +" Seconds)"
			print ('''				</h6>
									<p>
				  ''')
		for x in results_bm25:
			print ('''
									<div class="result-panel-heading">
										<div class="result_title">
											<h6 class="result-title-heading">
												<a href="''')
			print x['path'].encode('utf-8')
			print ('''"							>
				  ''')
			print x['title'].encode('utf-8')
			print ('''							</a>
		                                                                            <input id="switch-size"class="bmRel" value="rel" type="checkbox" data-size="mini">
											</h6>
											<h6 class="result-title-path">	
				  ''')
			print x['path'].encode('utf-8')

			print ('''						</h6>
										</div>
										<div class="result-panel-body">
				  ''')							
			print x.highlights("content",top=20).encode('utf-8')
			print ('''					</div>
									</div>
				''')
	print ('''				</p>
						</div>
						<div id="an" class="tab-pane fade">''')
	print ('''
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Index Size Vs Stop Word</h3>
                </div>
                <div class="analytics-panel-body">
                    Size of Index With Stop Word Removal: 224.8 Mb<br>
                    Size of Index Without Stop Word Removal: 237.3 Mb<br>
                    Increase in Index Size: 5.8 %<br>
                </div>
            </div>''')
	print	('''
            <div class="panel panel-default">
                <div class="panel-heading">
                    <h3 class="panel-title">Latency Time Vs Query Size</h3>
                </div>
                <div class="analytics-panel-body-graph">
                    <div id="container" style="width: 700px; height: 400px; margin: 0 auto"></div>
                </div>
            </div>''')
	print	('''
					</div>
					</div>
			</div>''')
	if doStem=="false":
		print ('''<script>document.getElementById("stem").checked = false;</script>''')
	else:
		print ('''<script>document.getElementById("stem").checked = true;</script>''')
	if doStop=="false":
		print ('''<script>document.getElementById("stop").checked = false;</script>''')
	else:
		print ('''<script>document.getElementById("stop").checked = true;</script>''')
	if int(count)==10000:
		print ('''<script>document.getElementById("nQ").disabled = true;
					document.getElementById("cal").disabled = true;
					document.getElementById("submitButton").disabled = true;
					document.getElementById("query").readOnly = true;
		</script>''')
	print('''
            <script>
                function hitOption(choice){
                    document.getElementById("hiddenOption").value = choice;
                   document.getElementById("myForm").submit();
                }
                function nextQuery(){
                    var tfRel = document.getElementsByClassName("tfRel");
                    var tfidfRel = document.getElementsByClassName("tfidfRel");
                    var bmRel = document.getElementsByClassName("bmRel");
                    var prevTf = document.getElementById("relTf").value;
                    var prevTfidf = document.getElementById("relTfidf").value;
                    var prevBm = document.getElementById("relBm").value;
                    var prevCount = document.getElementById("numQ").value;
                    /**for tf**/
                    var arr=[];
                    var rel = 0;
                    var tot = 0;
                    for (i = 0; i < tfRel.length; i++) {
                        tot++;
                        if(tfRel[i].checked==true){
                            /*this means this is a relevant document*/
                            rel++;
                            rel = rel;
                            tot = tot;
                            var x = 1.0*rel;
                            var y = 1.0*tot;
                            arr.push(x/y);
                        }
                    }
                    var cumFreq = 0.0;
                    for (i=0;i<arr.length;i++){
                        cumFreq += arr[i];
                    }
                    if(arr.length!=0){
                        var newTf = (cumFreq/arr.length)
                        document.getElementById("relTf").value = (Number(prevCount)*Number(prevTf) + newTf).toString();
                    }
                    else{
                        document.getElementById("relTf").value = "0";
                    }
                    /**for tfidf**/
                     arr=[];
                    rel = 0;
                    tot = 0;
                    for (i = 0; i < tfidfRel.length; i++) {
                        tot++;
                        if(tfidfRel[i].checked==true){
                            /*this means this is a relevant document*/
                            rel++;
                            rel = rel;
                            tot = tot;
                            var x = 1.0*rel;
                            var y = 1.0*tot;
                            arr.push(x/y);
                        }
                    }
                    var cumFreq = 0.0;
                    for (i=0;i<arr.length;i++){
                        cumFreq += arr[i];
                    }
                    if(arr.length!=0){
                        var newTfidf = (cumFreq/arr.length);
                        document.getElementById("relTfidf").value = (Number(prevCount)*Number(prevTfidf) + newTfidf).toString();
                    }
                    else{
                        document.getElementById("relTfidf").value = "0";
                    }
                    /**for bm25**/
                    arr=[];
                    rel = 0;
                   	tot = 0;
                    for (i = 0; i < bmRel.length; i++) {
                        tot++;
                        if(bmRel[i].checked==true){
                            /*this means this is a relevant document*/
                            rel++;
                            rel = rel;
                            tot = tot;
                            var x = 1.0*rel;
                            var y = 1.0*tot;
                            arr.push(x/y);
                        }
                    }
                    var cumFreq = 0.0;
                    for (i=0;i<arr.length;i++){
                        cumFreq += arr[i];
                    }
                    if(arr.length!=0){
                        var newBm = (cumFreq/arr.length);
                        document.getElementById("relBm").value = (Number(prevCount)*Number(prevBm) + newBm).toString();
                    }
                    else{
                        document.getElementById("relBm").value = "0";
                    }
                    document.getElementById("numQ").value = (Number(prevCount)+1).toString();
                    document.getElementById("myForm").submit();
                }
                
                function calculate(){
                	var prevTf = document.getElementById("relTf").value;
                    var prevTfidf = document.getElementById("relTfidf").value;
                    var prevBm = document.getElementById("relBm").value;
                    var prevCount = document.getElementById("numQ").value;
                    document.getElementById("relTf").value = (Number(prevTf)/Number(prevCount)).toString()
                    document.getElementById("relTfidf").value = (Number(prevTfidf)/Number(prevCount)).toString()
                    document.getElementById("relBm").value = (Number(prevBm)/Number(prevCount)).toString()
                    document.getElementById("numQ").value = "10000";
                    document.getElementById("myForm").submit();
                }
                
            </script>
		</body>
		
	</html>
	''')

def getData():
	global flag,doStem,doStop,option,relTf,formData,relTfidf,relBm,count
	flag = 1
	formData = cgi.FieldStorage()
	doStem = formData.getvalue("stem")
	if doStem==None:
		doStem = "false"
	doStop = formData.getvalue("stop")
	option = formData.getvalue("hiddenOption")
	relTf = formData.getvalue("relTf")
	if relTf==None:
		relTf = "0"
	relTfidf = formData.getvalue("relTfidf")
	if relTfidf==None:
		relTfidf = "0";
	relBm = formData.getvalue("relBm")
	if relBm==None:
		relBm = "0"
	count = formData.getvalue("numQ")
	if count==None:
		count = "0"
	if option!=None:
		option = int(option)
	if doStop==None:
		doStop = "false"
	if "query" not in formData:
		flag = 0
		return ""
	else:
		try:
			q = formData.getvalue('query')
		except:
			pass
		return q

def searchModule(qq):
	global results_bm25, results_tfidf, results_tf, results ,idx, time_bm25, time_tfidf, time_tf
	results_bm25 =  results_tfidf = results_tf = results = []
	time_bm25 = time_tfidf = time_tf = None
	if flag == 1:
		if doStem!="false" and doStop!="false":
			idx = open_dir("Indexed/Index_stsw")
		elif doStem!="false" and doStop=="false":
			idx = open_dir("Indexed/Index_st")
		elif doStem=="false" and doStop!="false":
			idx = open_dir("Indexed/Index_sw")
		else:
			idx = open_dir("Indexed/Index") 
		qp = qparser.QueryParser("content", schema=idx.schema)
		q = qp.parse(unicode(qq))							#by default, the parser treats the words as if they were connected by AND
		s = idx.searcher()
		results 		= s.search(q)
		results.fragmenter.surround = 50
		start = time.time()
		results_bm25 	= idx.searcher().search(q)
		time_bm25 = (time.time()-start)
		results_bm25.fragmenter.surround = 50

		start = time.time()
		results_tfidf 	= idx.searcher(weighting=scoring.TF_IDF()).search(q)
		time_tfidf = (time.time()-start)
		results_tfidf.fragmenter.surround = 50

		start = time.time()
		results_tf 	= idx.searcher(weighting=scoring.Frequency()).search(q)
		time_tf = (time.time()-start)
		results_tf.fragmenter.surround = 50
def main():
	global query
	query = getData()
	if(option==0):
		print "Location:http://172.16.114.65/IR/cgiFiles/map.py"
	if option==1:
		print "Location:http://172.16.114.65/IR/cgiFiles/ndgc.py"
	if option==2:
		print "Location:http://172.16.114.65/IR/cgiFiles/search.py"
	print "Content-type:text/html; image/jpg"
	print
	searchModule(query)
	searchpage()
	
	
if __name__== "__main__":	
	main()
