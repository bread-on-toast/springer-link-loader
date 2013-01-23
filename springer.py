#!/usr/bin/python

import httplib
import sys
import os
import urllib2

url="link.springer.com"

links=[]

def usage():
	print "\n Downloadskript for Springerlink.com\n\nusage: ./springer.py <link>\n \n<link> = http://link.springer.com/<type of publication>/<DOI>\n"
linkavail=0
for arg in sys.argv:
	if "link.springer.com" in arg:
		links.append(arg.split("link.springer.com")[1])
		linkavail=1
if linkavail==0:
	usage()
	sys.exit("")
httpServ = httplib.HTTPConnection(url, 80)
httpServ.connect()

title=""
front=""
back=""
book=[]

for i in links:
	httpServ.request('GET', i)
	data=httpServ.getresponse().read()
	for ii in data.split("\n"):
		if "h1 id=\"title\"" in ii:
			title=ii
		if "href=" in ii:
			if "pdf" in ii and "pdf-link webtrekk-track" in ii:
				book.append(ii.split("/content/pdf/")[1].split("\" pageType")[0])
			if "bfm" in ii and front=="":
				front=ii.split("/content/pdf/")[1].split("\">")[0]
			if "bbm" in ii and back=="":
				back=ii.split("/content/pdf/")[1].split("\">")[0]
httpServ.close()


#download-function
def download(url,filename):
	webFile = urllib2.urlopen(url)
	localFile = open(filename, 'w')
	localFile.write(webFile.read())
	localFile.close()


jj="i"

#download parts 
filelist="front.pdf "
for i in book:
	jj=jj+"i"
	download("http://link.springer.com/content/pdf/"+i,jj+".pdf")
	print "downloading "+i
	filelist=filelist+jj+".pdf "

	
#download front- and back-matter
print "downloading front.pdf"
download("http://link.springer.com/content/pdf/"+front,"front.pdf")
print "downloading back.pdf"
download("http://link.springer.com/content/pdf/"+back,"back.pdf")
filelist=filelist+"back.pdf "

#compose command
command="pdftk "+filelist+" output "+title.split("title\">")[1].split("</h1>")[0].replace(" ","_")+".pdf >/dev/null"

#execute
os.system(command)
#cleanup
os.system("rm i*.pdf front.pdf back.pdf")
print "written to: "+title.split("title\">")[1].split("</h1>")[0].replace(" ","_")+".pdf"
