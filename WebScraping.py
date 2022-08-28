#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 20:42:01 2022

@author: JuanJose
"""

#conda install urllib
#pip install beautifulsoup4
#conda install beautifulsoup4
#conda install lxml
# conda install -c conda-forge/label/cf202003 mechanicalsoup
#pip install selenium

import pandas as pd   
import numpy as np
import re
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import lxml
import mechanicalsoup


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#set URl
url = "http://olympus.realpython.org/profiles/poseidon"
#open URL
page = urlopen(url)

#read HTML
html_bytes = page.read()
html = html_bytes.decode("utf-8")


# extract text from HTML with regular expressions 
url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")

pattern = "<title.*?>.*?</title.*?>"
match_results = re.search(pattern, html, re.IGNORECASE)
title = match_results.group()
title = re.sub("<.*?>", "", title) # Remove HTML tags

print(title)

# parse html with beatifulSoup
url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

#get_text() method get rid of the html tags, you can acces the tags of html as method objects of BeautifulSoup 
print(soup.get_text())
print(soup.title.get_text())

# find all tags that have src value
soup.find_all("img", src="/static/dionysus.jpg")


###### INTERACT WITH HTML FORMS ##### 

# first you have to start you headless browser (non graphical browser)
browser = mechanicalsoup.Browser()

# then you can browse in it with methods
url = "http://olympus.realpython.org/login"
page = browser.get(url)
#page is a Response object that stores the response from requesting the URL from the browser: <Response [200]>

html_text= page.soup

## interaction 
browser = mechanicalsoup.Browser()
url = "http://olympus.realpython.org/login"
login_page = browser.get(url)
login_html = login_page.soup
form = login_html.select("form")[0]

# then you have to input the user and passwordto the html 
form.select("input")[0]["value"] = "zeus"
form.select("input")[1]["value"] = "ThunderDude"

# lastly you have to submit the html request 
profiles_page = browser.submit(form, login_page.url)








#### SEPOL interaction 
browser = mechanicalsoup.Browser()
url = "https://www.sepol.hn/sepol-estadisticas-registro-fallecidos.php"
SEPOL_page = browser.get(url)
SEPOL_page_html=SEPOL_page.soup
form = SEPOL_page_html.select("form")[0]
form.select("select")[0]["value"] = "01"
form.select("select")[1]["value"] = "TODOS"
form.select("select")[2]["value"] = "SUICIDIOS"
form.select("select")[3]["value"] = "2013"
form.select("input")[0]["value"] = "01-01-2013"
form.select("input")[1]["value"] = "31-12-2013"
form.select("input")[2]["value"] = "SI"
form.select("div")[1]("a")
table_page = browser.submit(form, SEPOL_page.url)


table_page.soup
SEPOL_page_html

form.select("div")[1]("a")


#### SELENIUM 

driver = webdriver.Chrome()


