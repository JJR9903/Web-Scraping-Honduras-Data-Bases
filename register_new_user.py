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

from pyunitreport import HTMLTestRunner
import unittest
from selenium import webdriver


class RegisterNewUser(unittest.TestCase):

    def SetUp(self):
        self.driver = webdriver.Chrome(executable_path='./chromedriver')
        driver = self.driver
        driver.get("http://demo-store.seleniumacademy.com/")
        driver.implicitly_wait(10)
        driver.maximize_window()

    def new_user(self):
        driver = self.driver
        driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/div/a/span[2]').click()
        driver.find_element_by_link_text('Log In').click()
        driver.implicitly_wait(30)



    def tearDown(self):
        """ finaliza el codigo """
        self.driver.quit()

if __name__=="__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes',report_name='search-reports'))


