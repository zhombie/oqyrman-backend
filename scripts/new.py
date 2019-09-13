def replace(text):
    dic = {"а" : "a", "ә" : "a'", "б" : "b", "в" : "v", "г" : "g",\
           "ғ" : "g'", "д" : "d", "е" : "e", "ё" : "e", "ж" : "j",\
           "з" : "z", "и" : "i'", "й" : "i'", "к" : "k", "қ" : "q",\
           "л" : "l", "м" : "m", "н" : "n", "ң" : "n'", "о" : "o",\
           "ө" : "o'", "п" : "p", "р" : "r", "с" : "s", "т" : "t",\
           "у" : "y'", "ұ" : "u", "ү" : "u'", "ф" : "f", "х" : "h",\
           "һ" : "h", "ц" : "ts", "ч" : "c'", "ш" : "s'", "щ" : "s'",\
           "ъ" : "", "ы" : "y", "і" : "i", "ь" : "", "э" : "e",\
           "ю" : "i'y'", "я" : "i'a", \
           "А" : "A", "Ә" : "A'", "Б" : "B", "В" : "V", "Г" : "G",\
           "Ғ" : "G'", "Д" : "D", "Е" : "E", "Ё" : "E", "Ж" : "J",\
           "З" : "Z", "И" : "I'", "Й" : "I'", "К" : "K", "Қ" : "Q",\
           "Л" : "L", "М" : "M", "Н" : "N", "О" : "O", "Ө" : "O'",\
           "П" : "P", "Р" : "R", "С" : "S", "Т" : "T", "У" : "Y'",\
           "Ұ" : "U", "Ү" : "U'", "Ф" : "F", "Х" : "H", "Ц" : "Ts",\
           "Ч" : "C'", "Ш" : "S'", "Щ" : "S'", "Ы" : "Y", "І" : "I",\
           "Э" : "E", "Ю" : "I'y'", "Я" : "I'a"}

    for i, j in dic.iteritems():
        text = text.replace(i.decode("utf-8"), j)
    return text

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
print "Original Title:", title, "Latin Title", replace(title)
print "Original Author:", author, "Latin Author", replace(title)
print "URL:", root_url
print

# ------------ Create Directory ------------ DONE
path = title
try:
    os.makedirs(path)
    print "Folder", path, "created"
    print
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# ------------ Create Mimetype ------------ DONE   
file = open(path + "/mimetype", "w") 
file.write("application/epub+zip")
print "Mimetype created"
file.close() 
print

# ------------ Create Table of Contents ------------ DONE
toc_response = urllib2.urlopen("http://kitap.kz/media/kitap/307/book/" + book_id + "/toc.ncx")
toc_soup = BeautifulSoup(toc_response, "lxml")

with open(path + '/toc.ncx', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write(toc_soup.find("ncx").prettify().encode("utf-8"))
print "Table of contents created"
print

# ------------ Create Container ------------ DONE
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

# ------------ Create Contents List ------------ DONE
contents_response = urllib2.urlopen("http://kitap.kz/" + root_url)
contents_soup = BeautifulSoup(contents_response, "lxml")

#NOTE: need to change contributor
with open(path + '/content.opf', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write(contents_soup.find("package").prettify().encode("utf-8"))
print "Contents list created"
print

# ------------ Create Epub ------------ DONE
result = ""
for i in range(1, 17):
    url = "http://kitap.kz/media/kitap/307/book/" + book_id + "/content_" + str(i) + ".xhtml"
    response = urllib2.urlopen(url)
    
    soup = BeautifulSoup(response, "lxml")
    beautified = soup.prettify()

    print beautified.encode("utf-8")
    
    with open(path + '/content_' + str(i) + '.xhtml', 'w') as f:
        f.write(beautified.encode('utf-8'))
print "Epub created"
print

# ------------ Create Book ToC ------------ DONE
btoc_response = urllib2.urlopen("http://kitap.kz/media/kitap/307/book/" + book_id + "/book_toc.xhtml")
btoc_soup = BeautifulSoup(btoc_response, "lxml")

with open(path + '/book_toc.xhtml', 'w') as f:
    f.write(btoc_soup.prettify().encode("utf-8"))
print "Book ToC created"
print

# ------------ Create Stylesheet ------------ DONE
style_response = urllib2.urlopen("http://kitap.kz/media/kitap/307/book/" + book_id + "/stylesheet.css")
style_soup = BeautifulSoup(style_response, "lxml")

with open(path + '/stylesheet.css', 'w') as f:
    f.write(style_soup.find("p").text.encode("utf-8"))
print "Stylesheet created"
print

"""
# ------------ Create ZipFile ------------ 
import zipfile
zip = zipfile.ZipFile(title + ".zip", "w", zipfile.ZIP_DEFLATED)
print "Zipfile created"
print

for mimetype in os.listdir(path):
    if mimetype == "mimetype":
        try:
            zip.write(path + "/" + mimetype)
            print "Mimetype replaced"
        except IOError:
            None
zip.close()

zip = zipfile.ZipFile(title + ".zip", "a")
for container in os.listdir(path + "/META-INF"):
    if container == "container.xml":
        try:
            zip.write(path + "/" + "META-INF/" + container)
            print "Container.xml replaced"
        except IOError:
            None

for files in os.listdir(path):
    if files.endswith(".xhtml") or files.endswith(".opf") \
        or files.endswith(".css") or files.endswith(".ncx"):
            try:
                zip.write(path + "/" + files)
            except IOError:
                None
print "Other files replaced"    
zip.close()
"""
