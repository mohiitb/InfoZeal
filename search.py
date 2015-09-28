#!/usr/bin/python
import cgitb
from whoosh.qparser import QueryParser
from os import listdir					#for getting the list of all files inside a directory
from os.path import isfile,join			#for same as above
from whoosh.index import create_in,exists_in,open_dir		#for creating schema
from whoosh.fields import *				#for defining fields in schema
from whoosh import scoring, qparser, analysis, fields, formats, query, highlight, collectors
import cgi
from BeautifulSoup import BeautifulSoup	#for extracting only text
import sys
import os
import time
from time import ctime
import re
def searchpage():
	global results, time_tf
	temp_tf 	= int(pagenum_tf)
	temp_tfidf 	= int(pagenum_tfidf)
	temp_bm25 	= int(pagenum_bm25)
	tf = tfidf = bm25 = 0
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
			<script>
                        $(function () {
    $('#container').highcharts({
        chart: {
            type: 'line'
        },
        title: {
            text: 'Latency Time Vs Query Length'
        },
        subtitle: {
            text: 'Query used: "hello buddy how are you and train number going there"'
        },
        xAxis: {
            categories:  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            title : {
                text: 'Length of Query (in number of terms)'
            }
        },
        yAxis: {
            title: {
                text: 'Latency Time (in ms)'
            }
        },
        plotOptions: {
            line: {
                dataLabels: {
                    enabled: true
                },
                enableMouseTracking: true
            }
        },
        series: [{
            name: 'TF',
            data: [1.82, 2.26, 12.07,33.25, 59.11, 93.28, 106.43, 123.82, 145.44,165.39]
        },{
            name: 'TF-IDF',
            data: [2.66,2.97,12.17,32.99,57.27,93.37,109.05,126.74,151.40,168.34]
        },{
            name: 'BM-25',
            data: [3.89,2.62,13.03,34.09,59.37,96.27,111.56,126.73,149.73,170.25]
        }]
    });
});
                    </script>
			<title>InfoZeal</title>
		</head>
		<body> 
			<div class="panel panel-default">
				<div class="panel-heading">
					<form class="form-inline" id="search_form" role="form" action="#" method="post">
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
											<input type="text" class="search_box" name="query" value=
		  ''')
	print ("'" + query +"'")
	print ('''								>
											<input type="hidden" name="searchtime" id="searchtime" value=''')
	print ("'" + str(ctime()) +"'")
	print ('''>
											<input type="hidden" name="pagenumField_tf" id="pagenumField_tf">
											<input type="hidden" name="pagenumField_tfidf" id="pagenumField_tfidf">
											<input type="hidden" name="pagenumField_bm25" id="pagenumField_bm25"> 
											<span class="input-group-btn">
												<input type="submit" class="btn btn-default" onclick="gettime(''')
	print ("'" + str(ctime()) +"'")												
	print (''')">Search
											</span>
										</div>
									</div>
								</div>
								
							</div>
						</div>
						&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
						
						Stemming&nbsp&nbsp&nbsp<input class="form-control" name="stem" id="stem" value="stemming" type="checkbox">
						&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
						Stop Word&nbsp&nbsp&nbsp<input class="form-control" type="checkbox" name="stop" value="stopping" id="stop">
						&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
                                       
                                        <div class="btn-group">
                                            <button type="button" class="btn btn-primary">Options</button>
                                                <button type="button" class="btn btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                <span class="caret"></span>
                                                <span class="sr-only">Toggle Dropdown</span>
                                            </button>
                                            <ul class="dropdown-menu">
                                                <li><a onclick="hitOption(1)">MAP</a></li>
                                                <li><a onclick="hitOption(2)">NDCG</a></li>
                                            </ul>
                                        </div>
						</div>
						</div>
				</form>
				<div class="result-panel-body-main">
					<ul class="nav nav-tabs">
					  <li class="active"><a data-toggle="tab" href="#tf">Term Frequency</a></li>
					  <li ><a data-toggle="tab" href="#tfidf">Invert Document Term Frequency</a></li>
					  <li ><a data-toggle="tab" href="#bm25">Best Match 25</a></li>
					  <li ><a data-toggle="tab" href="#an">Analytics</a></li>
					</ul>
					<div class="tab-content">
						<div id="tf" class="tab-pane fade in active">
							<h6>&nbsp&nbsp
		  ''')
	if time_tf is not None:
		print str(len(results_tf)) + " results (" + str(time_tf) +" seconds)"
	print ('''				</h6>
							<p>
		  ''')
	for x in results_tf:
		tf = tf + 1
		print ('''
								<div class="result-panel-heading">
									<div class="result_title">
										<h6 class="result-title-heading">
											<a 
			    data-time= ''')
		print "'" + str(searchtime) + "'"
		print ('''
				data-clicktime=
			''')
		print "'" + str(ctime()) + "'"
		print ('''
				data-query=
			''')
		print "'" + str(query) + "'"
		print ('''
				data-tech=
			''')
		print "TF"
		print ('''
				data-title=
			''')
		print "'" + str(x['title'].encode('utf-8')) + "'"
		print ('''
				data-path=
			''')
		print "'" + str(x['path'].encode('utf-8')) + "'"
		print ('''
				data-page=
			''')
		print str(temp_tf)
		print ('''
				data-result=
			''')
		print str(tf)
		print (''' class="link" href="
			  ''')
		print x['path'].encode('utf-8')
		print ('''							" >
			  ''')
		print x['title'].encode('utf-8')
		print ('''							</a>
										</h6>
										<h6 class="result-title-path">	
			  ''')
		print x['path'].encode('utf-8')

		print ('''						</h6>
									</div>
									<div class="result-panel-body">
			  ''')							
		print x.highlights("content",top=100).encode('utf-8')
		print ('''					</div>
								</div>
			''')
	if len(results_tf)>10:	
		print ('''					
							<nav class="results-pagination">
							  <ul class="pagination" name="page">
							    
			  ''')
		if temp_tf!=1:
				print ('''
								<li>
							      <a onclick="submitPage_tf(

					  ''')
				print (temp_tf-1)
				print (''' 			)" aria-label="Previous">
							        <span aria-hidden="true">&laquo;</span>
							      </a>
					  ''')

		if temp_tf%10!=0:
			for i in range(int(temp_tf/10)*10+1,min(int(temp_tf/10)*10+11,int(temp_tf/10)*10+int(total_tf)-int(temp_tf/10)*10+1)):
					if i==temp_tf:
						print ('''
									<li class="active">
							  ''')
					else:
						print ('''	<li>	''')
					print ('''		<a onclick="submitPage_tf(	''')
					print i		
					print ('''		)">''')
					print str(i)
					print ('''		</a>
								</li>
						  ''')
		else:
			for i in range(int((temp_tf-1)/10)*10+1,temp_tf+1):
				if i==temp_tf:
					print ('''
								<li class="active">
						  ''')
				else:
					print ('''	<li>	''')
				print ('''		<a onclick="submitPage_tf(	''')
				print i		
				print ('''		)">''')
				print str(i)
				print ('''		</a>
							</li>
					  ''')
		if (temp_tf+1)<=int(total_tf):
			print ('''		      
						    <li>
						      <a onclick="submitPage_tf(
				  ''')
			print (temp_tf+1)
			print ('''		  )" aria-label="Next">
						        <span aria-hidden="true">&raquo;</span>
						      </a>
						    </li>
			
				  ''')	
		
		print ('''				    
							  </ul>
							</nav>
			  ''')
		

	
	print ('''				</p>
		  ''')				
	print ('''			</div>
						<div id="tfidf" class="tab-pane fade">
						<h6>&nbsp&nbsp
			  ''')

	if time_tfidf is not None:
		print str(len(results_tfidf)) + " results (" + str(time_tfidf) +" Seconds)"
	print ('''				</h6>
							<p>
		  ''')
	for x in results_tfidf:
		tfidf = tfidf + 1
		print ('''
								<div class="result-panel-heading">
									<div class="result_title">
										<h6 class="result-title-heading">
											<a 
			    data-time= ''')
		print "'" + str(searchtime) + "'"
		print ('''
				data-clicktime=
			''')
		print "'" + str(ctime()) + "'"
		print ('''
				data-query=
			''')
		print query
		print ('''
				data-tech=
			''')
		print "TFIDF"
		print ('''
				data-title=
			''')
		print str(x['title'].encode('utf-8'))
		print ('''
				data-path=
			''')
		print str(x['path'].encode('utf-8'))
		print ('''
				data-page=
			''')
		print str(temp_tfidf)
		print ('''
				data-result=
			''')
		print str(tfidf)
		print (''' class="link" href="
			  ''')
		print x['path'].encode('utf-8')
		print ('''"							>
			  ''')
		print x['title'].encode('utf-8')
		print ('''							</a>
										</h6>
										<h6 class="result-title-path">	
			  ''')
		print x['path'].encode('utf-8')

		print ('''						</h6>
									</div>
									<div class="result-panel-body">
			  ''')							
		print x.highlights("content",top=100).encode('utf-8')
		print ('''					</div>
								</div>
			''')
	if len(results_tfidf)>10:	
		print ('''					
							<nav class="results-pagination">
							  <ul class="pagination" name="page">
							    
			  ''')
		if temp_tfidf!=1:
				print ('''
								<li>
							      <a onclick="submitPage_tfidf(

					  ''')
				print (temp_tfidf-1)
				print (''' 			)" aria-label="Previous">
							        <span aria-hidden="true">&laquo;</span>
							      </a>
					  ''')

		if temp_tfidf%10!=0:
			for i in range(int(temp_tfidf/10)*10+1,min(int(temp_tfidf/10)*10+11,int(temp_tfidf/10)*10+int(total_tfidf)-int(temp_tfidf/10)*10+1)):
					if i==temp_tfidf:
						print ('''
									<li class="active">
							  ''')
					else:
						print ('''	<li>	''')
					print ('''		<a onclick="submitPage_tfidf(	''')
					print i		
					print ('''		)">''')
					print str(i)
					print ('''		</a>
								</li>
						  ''')
		else:
			for i in range(int((temp_tfidf-1)/10)*10+1,temp_tfidf+1):
				if i==temp_tfidf:
					print ('''
								<li class="active">
						  ''')
				else:
					print ('''	<li>	''')
				print ('''		<a onclick="submitPage_tfidf(	''')
				print i		
				print ('''		)">''')
				print str(i)
				print ('''		</a>
							</li>
					  ''')
		if (temp_tfidf+1)<=int(total_tfidf):
			print ('''		      
						    <li>
						      <a onclick="submitPage_tfidf(
				  ''')
			print (temp_tfidf+1)
			print ('''		  )" aria-label="Next">
						        <span aria-hidden="true">&raquo;</span>
						      </a>
						    </li>
			
				  ''')	
		
		print ('''				    
							  </ul>
							</nav>
			  ''')
	print ('''				</p>
		  ''')				
	print ('''			</div>
						<div id="bm25" class="tab-pane fade">
							<h6>&nbsp&nbsp''')
	if time_bm25 is not None:
		print str(len(results_bm25)) + " results (" + str(time_bm25) +" Seconds)"
	print ('''				</h6>
							<p>
		  ''')
	for x in results_bm25:
		bm25 = bm25 + 1
		print ('''
								<div class="result-panel-heading">
									<div class="result_title">
										<h6 class="result-title-heading">
											<a 
			    data-time= ''')
		print "'" + str(searchtime) + "'"
		print ('''
				data-clicktime=
			''')
		print "'" + str(ctime()) + "'"
		print ('''
				data-query=
			''')
		print query
		print ('''
				data-tech=
			''')
		print "BM25"
		print ('''
				data-title=
			''')
		print str(x['title'].encode('utf-8'))
		print ('''
				data-path=
			''')
		print str(x['path'].encode('utf-8'))
		print ('''
				data-page=
			''')
		print str(temp_bm25)
		print ('''
				data-result=
			''')
		print str(bm25)
		print (''' class="link" href="
			  ''')
		print x['path'].encode('utf-8')
		print ('''"							>
			  ''')
		print x['title'].encode('utf-8')
		print ('''							</a>
										</h6>
										<h6 class="result-title-path">	
			  ''')
		print x['path'].encode('utf-8')

		print ('''						</h6>
									</div>
									<div class="result-panel-body">
			  ''')							
		print x.highlights("content",top=100).encode('utf-8')
		print ('''					</div>
								</div>
			''')
	if len(results_bm25)>10:	
		print ('''					
							<nav class="results-pagination">
							  <ul class="pagination" name="page">
							    
			  ''')
		if temp_bm25!=1:
				print ('''
								<li>
							      <a onclick="submitPage_bm25(

					  ''')
				print (temp_bm25-1)
				print (''' 			)" aria-label="Previous">
							        <span aria-hidden="true">&laquo;</span>
							      </a>
					  ''')

		if temp_bm25%10!=0:
			for i in range(int(temp_bm25/10)*10+1,min(int(temp_bm25/10)*10+11,int(temp_bm25/10)*10+int(total_bm25)-int(temp_bm25/10)*10+1)):
					if i==temp_bm25:
						print ('''
									<li class="active">
							  ''')
					else:
						print ('''	<li>	''')
					print ('''		<a onclick="submitPage_bm25(	''')
					print i		
					print ('''		)">''')
					print str(i)
					print ('''		</a>
								</li>
						  ''')
		else:
			for i in range(int((temp_bm25-1)/10)*10+1,temp_bm25+1):
				if i==temp_bm25:
					print ('''
								<li class="active">
						  ''')
				else:
					print ('''	<li>	''')
				print ('''		<a onclick="submitPage_bm25(	''')
				print i		
				print ('''		)">''')
				print str(i)
				print ('''		</a>
							</li>
					  ''')
		if (temp_bm25+1)<=int(total_bm25):
			print ('''		      
						    <li>
						      <a onclick="submitPage_bm25(
				  ''')
			print (temp_bm25+1)
			print ('''		  )" aria-label="Next">
						        <span aria-hidden="true">&raquo;</span>
						      </a>
						    </li>
			
				  ''')	
		
		print ('''				    
							  </ul>
							</nav>
			  ''')
		

	
	print ('''				</p>
		  ''')				
	print ('''			</div>
						<div id="an" class="tab-pane fade">''')
	print('''
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
        print('''
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">Latency Time Vs Query Size</h3>
                    </div>
                    <div class="analytics-panel-body-graph">
                        <div id="container" style="width: 700px; height: 400px; margin: 0 auto"></div>
                    </div>
                </div>''')						
							
	print('''					</div>
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
	print('''
            <script>
                function hitOption(choice){
                    document.getElementById("hiddenOption").value = choice.toString();
                   document.getElementById("search_form").submit();
                }
            </script>''')
	print('''
		<script>
				function submitPage_tf(pageNumber){
					document.getElementById("pagenumField_tf").value = pageNumber
					document.getElementById("search_form").submit();
				}
				function submitPage_tfidf(pageNumber){
					document.getElementById("pagenumField_tfidf").value = pageNumber
					document.getElementById("search_form").submit();
				}
				function submitPage_bm25(pageNumber){
					document.getElementById("pagenumField_bm25").value = pageNumber
					document.getElementById("search_form").submit();
				}
				$(function()
	            {
	                $('.link').click(function(){
	                	$.ajax({
	                        url: "ajaxpost.py",
	                        type: "post",
	                        datatype:"json",
	                        data: {
		                        'querydatetime':($(this).data("time")),
		                        'clickdatetime':($(this).data("clicktime")),
		                        'query':($(this).data("query")),
	                        	'technique':($(this).data("tech")),
	                        	'title':($(this).data("title")),
	                        	'path':($(this).data("path")),
	                        	'pagenumber':($(this).data("page")),
	                        	'resultrank':($(this).data("result")),
	                        },
	                    });
	                });
	            });
				function gettime(time){
					document.getElementById("searchtime").value = time;
				}

		</script>
		</body>
	</html>
	''')

def getData():
	global flag,doStem,doStop,pagenum_tf, pagenum_tfidf,pagenum_bm25, total_tf, total_tfidf, total_bm25,option,searchtime

	total_tf = 1
	total_tfidf = 1
	total_bm25 = 1
	flag = 1
	formData 		= cgi.FieldStorage()
	doStem 			= formData.getvalue("stem")
	pagenum_tf 		= formData.getvalue("pagenumField_tf")
	pagenum_tfidf 	= formData.getvalue("pagenumField_tfidf")
	pagenum_bm25 	= formData.getvalue("pagenumField_bm25")
	searchtime 		= formData.getvalue("searchtime")
	if searchtime==None:
		searchtime="ahha"
	if pagenum_tf==None:
		pagenum_tf = 1
	if pagenum_tfidf==None:
		pagenum_tfidf = 1
	if pagenum_bm25==None:
		pagenum_bm25 = 1	
	if doStem==None:
		doStem = "false"
	doStop = formData.getvalue("stop")
	if doStop==None:
		doStop = "false"
	option = formData.getvalue("hiddenOption")
	if option!=None:
		option = int(option)
	if "query" not in formData:
		flag = 0
		return ""
	else:
		try:
			q = formData.getvalue('query')
		except:
			pass
		return q

def searchModule(qq,pagenum_tf, pagenum_tfidf, pagenum_bm25,pagelength):
	global results_bm25, results_tfidf, results_tf, results ,idx, time_bm25, time_tfidf, time_tf, total_tf, total_tfidf, total_bm25
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
		
		start 			= time.time()
		results_bm25 	= idx.searcher().search_page(q, pagenum_bm25, pagelen=pagelength)
		time_bm25 		= (time.time()-start)
		#results_bm25.fragmenter.surround = 35

		start 			= time.time()
		results_tfidf 	= idx.searcher(weighting=scoring.TF_IDF()).search_page(q, pagenum_tfidf, pagelen=pagelength)
		time_tfidf 		= (time.time()-start)
		#results_tfidf.fragmenter.surround = 35
		
		start	 		= time.time()
		results_tf 		= idx.searcher(weighting=scoring.Frequency()).search_page(q, int(pagenum_tf), pagelen=pagelength)
		time_tf 		= (time.time()-start)
		#results_tf.fragmenter.surround = 35

		if len(results_tf)%10==0:
			total_tf = len(results_tf)/10
		else:
			total_tf = len(results_tf)/10 + 1

		if len(results_tfidf)%10==0:
			total_tfidf = len(results_tfidf)/10
		else:
			total_tfidf = len(results_tfidf)/10 + 1

		if len(results_bm25)%10==0:
			total_bm25 = len(results_bm25)/10
		else:
			total_bm25 = len(results_bm25)/10 + 1
		

def main():
	global query
	query = getData()
	if option==1:
		print "Location: http://172.16.114.65/IR/cgiFiles/map.py"
	if option==2:
		print "Location: http://172.16.114.65/IR/cgiFiles/ndgc.py"
	print "Content-type:text/html; image/jpg"
	print
	searchModule(query,pagenum_tf, pagenum_tfidf, pagenum_bm25,10)
	searchpage()
	
	
if __name__== "__main__":	
	main()
