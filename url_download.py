
from urllib2 import Request, urlopen, URLError
import os
from replace_file import replace

def download_html(url,filename,count):
	req = Request(line)
	#Start with line no 1
	try:
		response = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'Line No:', count, ':',e
		elif hasattr(e, 'code'):
			print 'Line No:', count, ':',e
	else:
		print 'Line No:', count, ' Downloading'+filename

		f = response.read()
		if filename is None:
			filename = 'index'
		output = open(os.path.join('test_'+str(count), filename), 'wb')
		output.write(f)
		output.close()
		return f


def download_assets(url,filename,path):
	path = path
	req_url = url
	print req_url
	req = Request(req_url)
	#Start with line no 1
	try:
		response = urlopen(req)
	except URLError as e:
		if hasattr(e, 'reason'):
			print 'FileName', filename, ':',e
		elif hasattr(e, 'code'):
			print 'FileName:', filename, ':',e
	else:
		print ' Downloading : '+filename
		f = response.read()
		if filename is None:
			filename = 'index'
		output = open(os.path.join(path, filename), 'wb')
		output.write(f)
		output.close()
		return f


count = 0
with open("urllist.txt", "r") as fil:
	for line in fil:
		line = line.rstrip()
		count = count+1
		print "Reading Line no : ",count

		#Create a new folder for writing the contents of this url
		if not os.path.exists('test_'+str(count)):
			os.makedirs('test_'+str(count))

		f = download_html(line,'test_'+str(count)+'.html',count)


		from BeautifulSoup import BeautifulSoup, SoupStrainer
		import re
		soup = BeautifulSoup(f)

		#Load all the scripts in the html page
		for script in soup.findAll(src=re.compile("\w+.js")):
			if script is not None:
				if (script["src"]).startswith('/'):
					path_js = 'test_'+str(count)+script.get('src')[:script.get('src').rfind('/'):]
					js_file_name = script["src"].split("/")[-1]
					if ".com" in line:
						js_file_path = line[:line.rfind('com')+3:]
					elif ".org" in line:
						js_file_path = line[:line.rfind('org')+3:]
					elif ".net" in line:
						js_file_path = line[:line.rfind('net')+3:]
					#Create a new folder for writing the contents of this url
					if not os.path.exists(path_js):
						os.makedirs(path_js)

					download_assets(js_file_path+script.get('src')[:script.get('src').rfind('/'):]+'/'+js_file_name,js_file_name,path_js)
				else:
					pass


		#Load all the CSS in the html page
		for style in soup.findAll(href=re.compile("\w+.css")):
			if style is not None:
				if (style["href"]).startswith('/'):
					path_css = 'test_'+str(count)+style.get('href')[:style.get('href').rfind('/'):]
					css_file_name = style["href"].split("/")[-1]
					if ".com" in line:
						css_file_path = line[:line.rfind('com')+3:]
					elif ".org" in line:
						css_file_path = line[:line.rfind('org')+3:]
					elif ".net" in line:
						css_file_path = line[:line.rfind('net')+3:]

					#Create a new folder for writing the contents of this url
					if not os.path.exists(path_css):
						os.makedirs(path_css)

					download_assets(css_file_path+style.get('href')[:style.get('href').rfind('/'):]+'/'+css_file_name,css_file_name,path_css)
				else:
					pass

		#Once all done replace the / or ../ with '', so that all the script tags will work fine
		replace(os.path.join('test_'+str(count), 'test_'+str(count)+'.html'), '="/', '="')
		replace(os.path.join('test_'+str(count), 'test_'+str(count)+'.html'), '../', '')

