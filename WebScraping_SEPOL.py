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

python3 WebScraping_SEPOL.py

#desactivar el ambiente virtual
deactivate
"""

import os
os.system("cd '/Users/JuanJose/Documents/Devops/Web Scraping Honduras DataBases/Web-Scraping-Honduras-Data-Bases'")
os.system("pip install pandas")
os.system("source venv/bin/activate")
os.system("pip install bs4")
os.system("pip install selenium")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup



chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
chrome_options.headless = True

driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
driver.get("https://www.sepol.hn/sepol-estadisticas-registro-fallecidos.php")
driver.maximize_window()



SEPOL=pd.DataFrame(columns=['Depto','Tipo Muerte','Año','Edad0_5','Edad6_10','Edad11_14','Edad15_18'])

"""
loop
"""

Deptos= ['ATLÁNTIDA', 'COLON', 'COMAYAGUA','COPAN','CORTES','CHOLUTECA','EL PARAÍSO','FANCISCO MORAZÁN','GRACIAS A DIOS','INTIBUCÁ','ISLAS DE LA BAHÍA','LA PAZ','LEMPIRA','OCOTEPEQUE','OLANCHO','SANTA BÁRBARA','VALLE','YORO']
delito = ['suicidios','homicidios']
años = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']

for año in años: 
    for depto in Deptos:
        for delito in delito: 
            
            #escoge la categoria de las estadisticas
            driver.find_element_by_id('incact_cod').send_keys(delito)
            #escoge el año de referencia
            driver.find_element_by_id('anio').send_keys(año)
            #escoge el departamento
            driver.find_element_by_id('dep_cod').send_keys(depto)

            # va y escoge la fecha de inicio 
            driver.find_element_by_id('fch_inicio').click()
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]').click()
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]').send_keys('Ene')
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[1]/td[3]').click()

            # va y escoge la fecha final 
            driver.find_element_by_id('fch_fin').click()
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]').click()
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div/div/select[1]').send_keys('Dic')
            driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/table/tbody/tr[5]/td[3]').click()
            driver.find_element_by_xpath('//*[@id="contactform"]/ol/li[7]/div/a').click()
            driver.find_element_by_xpath('//*[@id="tabs-two"]/ul/li[3]/a').click()

            tabla = driver.find_element_by_xpath('//*[@id="tab-two3"]/div/table').text

            Edad0_5=int(driver.find_element_by_xpath('//*[@id="tab-two3"]/div/table/tbody/tr[3]/td[2]').text)
            Edad6_10=int(driver.find_element_by_xpath('//*[@id="tab-two3"]/div/table/tbody/tr[4]/td[2]').text)
            Edad11_14=int(driver.find_element_by_xpath('//*[@id="tab-two3"]/div/table/tbody/tr[5]/td[2]').text)
            Edad15_18=int(driver.find_element_by_xpath('//*[@id="tab-two3"]/div/table/tbody/tr[6]/td[2]').text)

            df = pd.DataFrame(data={'Depto': [depto], 'Año':año ,'Tipo Muerte': delito, 'Edad0_5':Edad0_5,'Edad6_10':Edad6_10,'Edad11_14':Edad11_14,'Edad15_18':Edad15_18})

            SEPOL = pd.concat([SEPOL, df])

driver.quit()

SEPOL['-18'] = SEPOL.iloc[:,3:7].sum(axis=1)


print(SEPOL)

SEPOL.to_excel("/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos/SEPOL.xlsx", sheet_name="SEPOL",index=False)






