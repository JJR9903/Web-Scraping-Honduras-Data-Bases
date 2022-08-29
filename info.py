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


#desactivar el ambiente virtual
deactivate

"""
#!pip install pyunitreport
#!pip install selenium


import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver

class HelloWorld(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """prepara el entrono de prueba """
        cls.driver = webdriver.Chrome(executable_path= r'./chromedriver')
        driver= cls.driver
        driver.implicitly_wait(10)
        

    def test_hello_world(self):
        """ realiza acciones """
        driver = self.driver
        driver.get('https://www.platzi.com')

    def test_wikipedia(self):
        """ realiza acciones """
        driver = self.driver
        driver.get('https://es.wikipedia.org/wiki/Wikipedia:Portada')


    @classmethod
    def tearDownClass(cls):
        """ finaliza el codigo """
        cls.driver.quit()


if __name__=="__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes',report_name='hello-world-report'))

