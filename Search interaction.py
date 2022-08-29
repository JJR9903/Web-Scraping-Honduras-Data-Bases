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


from itertools import product
from lib2to3.pgen2 import driver
from re import search
from tkinter import Button
import unittest
from pyunitreport import HTMLTestRunner
from selenium import webdriver

class SearchTest(unittest.TestCase):

    
    def setUp(self):
        """prepara el entrono de prueba """
        self.driver = webdriver.Chrome(executable_path= './chromedriver')
        driver= self.driver
        driver.get("http://demo-store.seleniumacademy.com/")
        driver.maximize_window()
        driver.implicitly_wait(10)

    def test_search_Tshirt(self):
        """ va al buscador de la pagina web (de nombre 'q'), teclea una palabra ('tee') y ejecuta la busqueda"""
        driver = self.driver
        search_field = driver.find_element_by_name('q')
        search_field.clear()

        search_field.send_keys('tee')
        search_field.submit()

    def test_search_salt_shaker(self):
        """ va al buscador de la pagina web (de nombre 'q'), teclea una palabra ('salt shaker') y ejecuta la busqueda"""
        driver = self.driver
        search_field = driver.find_element_by_name('q')
        search_field.clear()

        search_field.send_keys('salt shaker')
        search_field.submit()
        products= driver.find_elements_by_xpath('//*[@id="top"]/body/div/div[2]/div[2]/div/div[2]/div[2]/div[3]/ul/li/div/h2/a')
        self.assertEqual(1,len(products))


    def test_search_text_field(self):
        """ busca un element tag por el id  """
        search_field= self.driver.find_element_by_id("search")
       
    def test_search_text_field_by_name(self):
        """ busca un element tag por su nombre  """
        search_field= self.driver.find_element_by_name("q")

    def test_search_text_field_by_class_name(self):
        """ busca un element tag por su clase  """
        search_field= self.driver.find_element_by_class_name("input-text")

    def test_search_button_enabled(self):
        """ busca un ibjeto tipo boton """
        Button = self.driver.find_element_by_class_name("button")

    def test_count_of_promo_banner_images(self):
        """ busca cuantos banner images hay de promos """
        banner_list = self.driver.find_element_by_class_name("promos")
        banners = banner_list.find_element_by_tag_name('img')
        self.assertEqual(3, len(banners)) 

    def test_vip_promo(self):
        """ identifica una imagen por su xpath """
        vip_promo = self.driver.find_element_by_xpath('//*[@id="top"]/body/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[4]/a/img')

    def test_shopping_car(self):
        """ identifica el icono del carro de compras por el css """
        shopping_car = self.driver.find_element_by_css_selector("div.header-minicart span.icon")

    def tearDown(self):
        """ finaliza el codigo """
        self.driver.quit()


if __name__=="__main__":
    unittest.main(verbosity=2, testRunner=HTMLTestRunner(output='reportes',report_name='search-reports'))

