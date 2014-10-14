
from urllib2 import Request, urlopen, URLError
import os
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re


def download_assets(url,filename):
	req = Request(url)
	#Start with line no 1
	try:
		response = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'File Name:', filename, 'not downloaded due to : ',e
		elif hasattr(e, 'code'):
			print 'File Name:', filename, 'not downloaded due to : ',e
	else:
		print 'Downloading file : '+filename

		f = response.read()
		if filename is None:
			filename = 'index'
		output = open(os.path.join(folder, filename), 'wb')
		output.write(f)
		output.close()

def return_html(url):
	req = Request(url)
	#Start with line no 1
	try:
		response = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'Error:',e
		elif hasattr(e, 'code'):
			print 'Error:',e
	else:
		print 'Reading '+url
		f = response.read()
		return f


url = "https://class.coursera.org/algo-004/lecture"
folder = "algo"
#course-topbanner-name
if not os.path.exists(folder):
	os.makedirs(folder)

f = return_html(url)
soup = BeautifulSoup(f)

#Load all the scripts in the html page
for lists in soup.findAll('a',{'class':"lecture-link"}):
	#the url of the iframe in the given webpage
	res_lis = urlopen(Request(lists.get('data-modal-iframe')))
	vid = res_lis.read()
	actual_lis = BeautifulSoup(vid)
	videos = actual_lis.findAll('source',{'type':'video/webm'})
	download_url_value = str(videos[0])
	download_assets(download_url_value[31:download_url_value.rfind("webm")+4:],lists.text)


