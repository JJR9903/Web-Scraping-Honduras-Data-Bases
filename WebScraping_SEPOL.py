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
python3 -m pip install openpyxl

python3 WebScraping_SEPOL.py

#desactivar el ambiente virtual
deactivate
"""

#import os
#os.system("pip install pandas")
#os.system("cd '/Users/JuanJose/Documents/Devops/Web Scraping Honduras DataBases/Web-Scraping-Honduras-Data-Bases'")
#os.system("source venv/bin/activate")
#os.system("pip install bs4")
#os.system("pip install selenium")
#os.system("pip install openpyxl")

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException





chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
chrome_options.headless = True

driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
driver.get("https://www.sepol.hn/sepol-estadisticas-registro-fallecidos.php")
driver.maximize_window()
action = ActionChains(driver)
wait = WebDriverWait(driver, 10)


SEPOL = pd.DataFrame(columns=['Depto','Año','Tipo Muerte','Edad0_5','Edad6_10','Edad11_14','Edad15_18'])

Deptos= ['ATLÁNTIDA', 'COLON', 'COMAYAGUA','COPAN','CORTES','CHOLUTECA','EL PARAÍSO','FANCISCO MORAZÁN','GRACIAS A DIOS','INTIBUCÁ','ISLAS DE LA BAHÍA','LA PAZ']
delitos = ['suicidios','homicidios']
años = ['2013','2014','2015','2016','2017','2018','2019','2020','2021','2022']


for año in años: 
    for depto in Deptos:
        for delito in delitos: 

            print(año,depto,delito)
            

            #escoge el departamento
            element = wait.until(EC.element_to_be_clickable((By.ID, 'dep_cod')))
            element.send_keys(depto)


            #escoge el año de referencia
            element = wait.until(EC.element_to_be_clickable((By.ID, 'anio')))
            element.send_keys(año)

            #escoge la categoria de las estadisticas
            element = wait.until(EC.element_to_be_clickable((By.ID, 'incact_cod')))
            element.send_keys(delito)

            driver.execute_script("window.scrollTo(0,0)")

            # va y escoge la fecha de inicio 
            element = wait.until(EC.element_to_be_clickable((By.ID, 'fch_inicio')))
            element.click()
            driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]').click()
            driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]').send_keys('Ene')
            dias = driver.find_elements(By.CLASS_NAME, 'ui-state-default')
            for i in dias:
                if i.text == "1":
                    i.click()


            driver.execute_script("window.scrollTo(0,0)")

            # va y escoge la fecha final 
            element = wait.until(EC.element_to_be_clickable((By.ID, 'fch_fin')))
            element.click()
            driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]').click()
            driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]').send_keys('Dic')
            dias = driver.find_elements(By.CLASS_NAME, 'ui-state-default')
            for i in dias:
                if i.text == "31":
                    i.click()
   


            driver.execute_script("window.scrollTo(0,0)")

            #escoge la categoria de las estadisticas
            element = wait.until(EC.element_to_be_clickable((By.ID, 'incact_cod')))
            element.send_keys(delito)
        

            # genera la tabla  
            element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contactform"]/ol/li[7]/div/a')))
            element.send_keys("\n")

            #class="error": No hay registros encontrados
            try: 
                driver.find_element(By.CLASS_NAME, 'error')
                print(año,depto,delito,"sin registros")
            except NoSuchElementException:

                # va a la tabla 
                element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs-two"]/ul/li[3]/a')))
                element.send_keys("\n")


                tabla = driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table').text

                Edad0_5=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[3]/td[2]').text)
                Edad6_10=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[4]/td[2]').text)
                Edad11_14=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[5]/td[2]').text)
                Edad15_18=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[6]/td[2]').text)

                df = pd.DataFrame(data={'Depto': [depto], 'Año':año ,'Tipo Muerte': delito, 'Edad0_5':Edad0_5,'Edad6_10':Edad6_10,'Edad11_14':Edad11_14,'Edad15_18':Edad15_18})

                SEPOL = pd.concat([SEPOL, df])

            print(año,depto,delito,"hecho")

driver.quit()

SEPOL['-18'] = SEPOL.iloc[:,3:7].sum(axis=1)


print(SEPOL)

SEPOL.to_excel("/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos/SEPOL.xlsx", sheet_name="SEPOL",index=False)




