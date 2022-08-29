# siempre antes de iniciar cualquier proyecto en python es una buena practica crear un ambiente virtual con una versión especifica de python y de sus modulos
"""
EN LA TERMINAL 

cd '/Users/JuanJose/Documents/Devops/Web Scraping Honduras DataBases/Web-Scraping-Honduras-Data-Bases'

#crear el ambiente virtual
python3 -m venv venv
#activar el ambiente virtual
source venv/bin/activate


###
pip install selenium==4.1.3
sudo apt-get install python3.9-venv

python3 -m pip install selenium
python3 -m pip install pyunitreport

#desactivar el ambiente virtual
deactivate
"""

from venv import create
from selenium import webdriver

driver = webdriver.Chrome(executable_path='./chromedriver')
driver.get("http://demo-store.seleniumacademy.com/")
driver.implicitly_wait(10)
driver.maximize_window()

driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div/a/span[2]').click()
driver.find_element_by_link_text('Log In').click()
driver.implicitly_wait(30)

create_account_button = driver.find_element_by_xpath('//*[@id="login-form"]/div/div[1]/div[2]/a').click()
