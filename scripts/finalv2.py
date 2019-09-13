# NOTE: CHANGE UPPERCASE/LOWERCASE WORDS 
# NOT FULL, NEED TO FINISH SAVING EPUB

import urllib2
from bs4 import BeautifulSoup
import re
import os, errno
import requests
from ebooklib import epub

def replace(text):
    dic = {"а" : "a", "ә" : "á", "б" : "b", "в" : "v", "г" : "g",\
           "ғ" : "ǵ", "д" : "d", "е" : "e", "ё" : "e", "ж" : "j",\
           "з" : "z", "и" : "ı", "й" : "ı", "к" : "k", "қ" : "q",\
           "л" : "l", "м" : "m", "н" : "n", "ң" : "ń", "о" : "o",\
           "ө" : "ó", "п" : "p", "р" : "r", "с" : "s", "т" : "t",\
           "у" : "ý", "ұ" : "u", "ү" : "ý", "ф" : "f", "х" : "h",\
           "һ" : "h", "ц" : "ts", "ч" : "ch", "ш" : "sh", "щ" : "sh",\
           "ъ" : "", "ы" : "y", "і" : "i", "ь" : "", "э" : "e",\
           "ю" : "ıý", "я" : "ıa", \
           "А" : "A", "Ә" : "Á", "Б" : "B", "В" : "V", "Г" : "G",\
           "Ғ" : "Ǵ", "Д" : "D", "Е" : "E", "Ё" : "E", "Ж" : "J",\
           "З" : "Z", "И" : "I", "Й" : "I", "К" : "K", "Қ" : "Q",\
           "Л" : "L", "М" : "M", "Н" : "N", "Ң" : "Ń", "О" : "O",\
           "Ө" : "Ó", "П" : "P", "Р" : "R", "С" : "S", "Т" : "T",\
           "У" : "Ý", "Ұ" : "U", "Ү" : "Ú", "Ф" : "F", "Х" : "H",\
           "Ц" : "Ts", "Ч" : "Ch", "Ш" : "Sh", "Щ" : "Sh", "Ы" : "Y",\
           "І" : "I", "Э" : "E", "Ю" : "Iý", "Я" : "Ia"}
    
    for i, j in dic.iteritems():
        text = text.replace(i.decode("utf-8"), j.decode("utf-8"))
        
    return text

general_book = "botagoz_mukanov"
general_response = urllib2.urlopen("http://kitap.kz/books/" + general_book)
general_soup = BeautifulSoup(general_response, "lxml")

name = general_soup.find("h3", {"class": "bookitem-info__name"})
author = general_soup.find("a", {"class": "bookitem-info__author"})
image = general_soup.find("img", {"class": "bookitem-book__img"})

img_src = image.attrs.values()[0]
book_id = img_src.split("/")[3]

url = "http://kitap.kz"

word = "BeRiNsHi"
ups = 0
lows = 0
for i in word:
    if i.isupper():
        ups += 1
    
if ups > 1:
    word = word.upper()
    print word

# ------------ Create Directory ------------
path = name.text
print "path", path
try:
    os.makedirs(path)
    print "Folder", path, "created"
    print
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

# ------------ Cover image download ------------
img_data = requests.get(url + img_src).content
with open(path + "/" + name.text + '.jpg', 'wb') as handler:
    handler.write(img_data)
print "Image", path + "/" + name.text + '.jpg', "created"
print "Latin image", replace(path + "/" + name.text + '.jpg')

# ------------ Original epub download ------------
epub_data = requests.get(url + "/uploads/books/" + book_id + "/File_book.epub").content
epub_path = path + "/" + name.text + '.epub'
with open(epub_path, 'wb') as handler:
    handler.write(epub_data)
print "Epub", epub_path, "created"
print "Latin epub", replace(epub_path)

# ------------ Write new contents ------------
book_epub = epub.read_epub(epub_path)

for item in book_epub.items:
    print epub_path, item.file_name
    
    file_name = item.file_name
    content = item.content
    
    try:
        with open(path+"/"+file_name, 'w') as f:
            f.write(content)
    except IOError:
        pass

# ------------ Translate to Latin ------------
counter = 0
for i in os.listdir(path):
    if "content" in i.encode("utf-8"):
        counter += 1

for i in range(1, counter + 1):
    res = ""
    file = open(path + "/content_" + str(i) + ".xhtml", "r") 
    for line in file: 
        res += replace(line.decode("utf-8"))
        
    try:
        os.makedirs(path + "/latin")
        print "folder", path, "/latin", "created"
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    with open(path + "/latin/content_" + str(i) + ".xhtml", "w") as f:   
        f.write(res.encode("utf-8")) 

# ------------ Write Epub ------------

book = epub.EpubBook()

# set metadata
book.set_identifier('id123456')
book.set_title('Sample book')
book.set_language('en')

book.add_author('Author Authorowski')
book.add_author('Danko Bananko', file_as='Gospodin Danko Bananko', role='ill', uid='coauthor')

# create chapter
c1 = epub.EpubHtml(title='Intro', file_name='chap_01.xhtml', lang='hr')
file = open(path + "/content_" + str(i) + ".xhtml", "r") 
c1.content=res.encode("utf-8")

# add chapter
book.add_item(c1)

# define Table Of Contents
book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
             (epub.Section('Simple book'),
             (c1, ))
            )

# add default NCX and Nav file
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# define CSS style
style = 'BODY {color: white;}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

# add CSS file
book.add_item(nav_css)

# basic spine
book.spine = ['nav', c1]

# write to the file
epub.write_epub('test.epub', book, {})
