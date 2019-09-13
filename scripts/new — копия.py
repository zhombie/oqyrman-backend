import urllib2
from bs4 import BeautifulSoup
import re
import os, errno

general_book = "botagoz_mukanov"
general_response = urllib2.urlopen("http://kitap.kz/reader/" + general_book)
general_soup = BeautifulSoup(general_response, "lxml")

script = general_soup.findAll("script")
title = script[1].text.split(",")[1].split(":")[1]
author = script[1].text.split(",")[2].split(":")[1]
root_url = script[1].text.split(",")[5].split(":")[1]

title = str(title.encode("utf-8")).strip().decode("utf-8").replace("'", "")
author = str(author.encode("utf-8")).strip().decode("utf-8").replace("'", "")
root_url = str(root_url.encode("utf-8")).strip().replace("'", "")
book_id = root_url.split("/")[5]

print "ID:", book_id
print "Title:", title
print "Author:", author
print "URL:", root_url
print

# ------------ Create Directory ------------
path = title
try:
    os.makedirs(path)
    print "Folder", path, "created"
    print
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# ------------ Create Mimetype ------------    
file = open(path + "/mimetype", "w") 
file.write("application/epub+zip")
print "Mimetype created"
file.close() 
print

# ------------ Create Table of Contents ------------    
toc_response = urllib2.urlopen("http://kitap.kz/media/kitap/307/book/" + book_id + "/toc.ncx")
toc_soup = BeautifulSoup(toc_response, "lxml")
with open(path + '/toc.ncx', 'w') as f:
    f.write(toc_soup.prettify().encode("utf-8"))
print "Table of contents created"
print

# ------------ Create Container ------------
meta_inf = path + "/META-INF"
try:
    os.makedirs(meta_inf)
    print "Folder", path, "created"
    print
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

file = open(path + "/META-INF/container.xml", "w") 
file.write('<?xml version="1.0" encoding="UTF-8"?>')
file.write('<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">')
file.write('<rootfiles>')
file.write('<rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>')
file.write('</rootfiles>')
file.write('</container>')
print "Container created"
file.close() 
print

# ------------ Create Contents List ------------
contents_response = urllib2.urlopen("http://kitap.kz/" + root_url)
contents_soup = BeautifulSoup(contents_response, "lxml")

#NOTE: need to change contributor
with open(path + '/content.opf', 'w') as f:
    f.write(contents_soup.prettify().encode("utf-8"))
print "Contents list created"
print

# ------------ Create Epub ------------
result = ""
for i in range(1, 17):
    url = "http://kitap.kz/media/kitap/307/book/" + book_id + "/content_" + str(i) + ".xhtml"
    print "parsing: ", url
    response = urllib2.urlopen(url)
    
    soup = BeautifulSoup(response, "lxml")
    beautified = soup.prettify()

    result += beautified
    
with open(path + '/output.txt', 'w') as f:
    f.write(result.encode('utf-8'))
