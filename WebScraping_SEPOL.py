# siempre antes de iniciar cualquier proyecto en python es una buena practica crear un ambiente virtual con una versión especifica de python y de sus modulos
"""
EN LA TERMINAL 

cd '/Users/JuanJose/Documents/Devops/Web Scraping Honduras DataBases/Web-Scraping-Honduras-Data-Bases/'

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

python3  WebScraping_SEPOL.py

#desactivar el ambiente virtual
deactivate
"""




from tracemalloc import start
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
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException





chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
chrome_options.headless = True
driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
driver.get("https://www.sepol.hn/sepol-estadisticas-registro-fallecidos.php")
driver.maximize_window()
action = ActionChains(driver)
wait = WebDriverWait(driver, 5)



def click_until_interactable(by,element):
    element_is_interactable= False
    counter= 1
    element=driver.find_element(by,element)

    while not element_is_interactable:
        try:
            element = wait.until(EC.element_to_be_clickable(element))
            element.click()
            element_is_interactable= True
        except (ElementNotInteractableException,ElementClickInterceptedException) as e:
            counter = counter +1 
            driver.execute_script("window.scrollTo(0,0)")
    return element_is_interactable 


SEPOL = pd.DataFrame(columns=['Depto','Mun','Año','Tipo Muerte','Edad0_5','Edad6_10','Edad11_14','Edad15_18'])

delitos = ['suicidios','homicidios']


Deptos= ['ATLÁNTIDA', 'COLON', 'COMAYAGUA', 'COPAN', 'CORTES', 'CHOLUTECA', 'EL PARAÍSO', 'FRANCISCO MORAZÁN', 'GRACIAS A DIOS', 'INTIBUCÁ', 'ISLAS DE LA BAHÍA', 'LA PAZ', 'LEMPIRA', 'OCOTEPEQUE', 'OLANCHO', 'SANTA BÁRBARA', 'VALLE', 'YORO']
municipios= {
    'ATLÁNTIDA':['LA CEIBA','EL PORVENIR','ESPARTA','JUTIAPA','LA MASICA','SAN FRANCISCO','TELA','ARIZONA'],
    'COLON':['TRUJILLO','BALFATE','IRIONA','LIMÓN','SABÁ','SANTA FE','SANTA ROSA DE AGUÁN','SONAGUERA','TOCOA','BONITO ORIENTAL'],
    'COMAYAGUA':['COMAYAGUA','AJUTERIQUE','EL ROSARIO','ESQUÍAS','HUMUYA','LA LIBERTAD','LAMANÍ','LA TRINIDAD','LEJAMANÍ','MEÁMBAR','MINAS DE ORO','OJOS DE AGUA','SAN JERÓNIMO','SAN JOSÉ DE COMAYAGUA',"LAS LAJAS", "SAN JOSÉ DEL POTRERO", "SAN LUIS", "SAN SEBASTIÁN", "SIGUATEPEQUE", "TAULABÉ", "VILLA DE SAN ANTONIO"],
    'COPAN':['SANTA ROSA DE COPÁN','CABAÑAS','CONCEPCIÓN','COPÁN RUINAS','CORQUÍN','CUCUYAGUA','DOLORES','DULCE NOMBRE','EL PARAÍSO','FLORIDA','LA JIGUA','LA UNIÓN','NUEVA ARCADIA','SAN AGUSTÍN','SAN ANTONIO','SAN JERÓNIMO','SAN JOSÉ','SAN JUAN DE OPOA','SAN NICOLÁS','SAN PEDRO DE COPÁN','SANTA RITA','TRINIDAD DE COPÁN','VERACRUZ'],
    'CORTES':['SAN PEDRO SULA','CHOLOMA','OMOA','PIMIENTA','POTRERILLOS','PUERTO CORTÉS','SAN ANTONIO DE CORTÉS','SAN FRANCISCO DE YOJOA','SAN MANUEL','SANTA CRUZ DE YOJOA','VILLANUEVA','LA LIMA'],
    'CHOLUTECA':['CHOLUTECA','APACILAGUA','CONCEPCIÓN DE MARIA','DUYURE','EL CORPUS','EL TRIUNFO','MARCOVIA','MOROLICA','NAMASIGUE','OROCUINA','PESPIRE','SAN ANTONIO DE FLORES','SAN ISIDRO','SAN JOSÉ','SAN MARCOS DE COLON','SANTA ANA DE YUSGUARE'],
    'EL PARAÍSO':['YUSCARÁN','ALAUCA','DANLÍ','EL PARAÍSO','GÜINOPE','JACALEAPA','LIURE','MOROCELÍ','OROPOLÍ','POTRERILLOS','SAN ANTONIO DE FLORES','SAN LUCAS','SAN MATÍAS','SOLEDAD','TEUPASENTI','TEXIGUAT','VADO ANCHO','YAUYUPE','TROJES'],
    'FRANCISCO MORAZÁN':['DISTRITO CENTRAL','ALUBAREN','CEDROS','CURARÉN','EL PORVENIR','GUAIMACA','LA LIBERTAD','LA VENTA','LEPATERIQUE','MARAITA','MARALE','NUEVA ARMENIA','OJOJONA','ORICA','REITOCA','SABANAGRANDE','SAN ANTONIO DE ORIENTE','SAN BUENAVENTURA','SAN IGNACIO','SAN JUAN DE FLORES','SAN MIGUELITO','SANTA ANA','SANTA LUCÍA','TALANGA','TATUMBLA','VALLE DE ANGELES','VILLA DE SAN FRANCISCO','VALLECILLO'],
    'GRACIAS A DIOS':['PUERTO LEMPIRA','BRUS LAGUNA','AHUAS','JUAN FRANCISCO BULNES','VILLEDA MORALES','WAMPUSIRPI'],
    'INTIBUCÁ':['LA ESPERANZA','CAMASCA','COLOMONCAGUA','CONCEPCIÓN','DOLORES','INTIBUCÁ','JESÚS DE OTORO','MAGDALENA','MASAGUARA','SAN ANTONIO','SAN ISIDRO','SAN JUAN','SAN MARCOS DE LA SIERRA','SAN MIGUELITO','SANTA LUCÍA','YAMARANGUILA','SAN FRANCISCO DE OPALACA'],
    'ISLAS DE LA BAHÍA':['ROATÁN','GUANAJA','JOSÉ SANTOS GUARDIOLA','UTILA'],
    'LA PAZ':['LA PAZ','AGUANQUETERIQUE','CABAÑAS','CANE','CHINACLA','GUAJIQUIRO','LAUTERIQUE','MARCALA','MERCEDES DE ORIENTE','OPATORO','SAN ANTONIO DEL NORTE','SAN JOSÉ','SAN JUAN','SAN PEDRO DE TUTULE','SANTA ANA','SANTA ELENA','SANTA MARÍA','SANTIAGO DE PURINGLA','YARULA'],
    'LEMPIRA':['GRACIAS','BELÉN','CANDELARIA','COLOLACA','ERANDIQUE','GUALCINCE','GUARITA','LA CAMPA','LA IGUALA','LAS FLORES','LA UNIÓN','LA VIRTUD','LEPAERA','MAPULACA','PIRAERA','SAN ANDRÉS','SAN FRANCISCO','SAN JUAN GUARITA','SAN MANUEL COLOHETE','SAN RAFAEL','SAN SEBASTIÁN','SANTA CRUZ','TALGUA','TAMBLA','TOMALÁ','VALLADOLID','VIRGINIA','SAN MARCOS DE CAIQUIN'],
    'OCOTEPEQUE':['OCOTEPEQUE','BELÉN GUALCHO','CONCEPCIÓN','DOLORES MERENDÓN','FRATERNIDAD','LA ENCARNACIÓN','LA LABOR','LUCERNA','MERCEDES','SAN FERNANDO','SAN FRANCISCO DEL VALLE','SAN JORGE','SAN MARCOS','SANTA FE','SENSENTI','SINUAPA'],
    'OLANCHO':['JUTICALPA','CAMPAMENTO','CATACAMAS','CONCORDIA','DULCE NOMBRE DE CULMÍ','EL ROSARIO','ESQUIPULAS DEL NORTE','GUALACO','GUARIZAMA','GUATA','GUAYAPE','JANO','LA UNIÓN','MANGULILE','MANTO','SALAMÁ','SAN ESTEBAN','SAN FRANCISCO DE BECERRA','SAN FRANCISCO DE LA PAZ','SANTA MARÍA DEL REAL','SILCA','YOCÓN','PATUCA'],
    'SANTA BÁRBARA':['SANTA BÁRBARA','ARADA','ATIMA','AZACUALPA','CEGUACA','CONCEPCIÓN DEL NORTE','CONCEPCIÓN DEL SUR','CHINDA','EL NÍSPERO','GUALALA','ILAMA','MACUELIZO','NARANJITO','NUEVO CELILAC','PETOA','PROTECCIÓN','QUIMISTÁN','SAN FRANCISCO DE OJUERA','SAN JOSÉ DE COLINAS','SAN LUIS','SAN MARCOS','SAN NICOLÁS','SAN PEDRO ZACAPA','SAN VICENTE CENTENARIO','SANTA RITA','TRINIDAD','LAS VEGAS','NUEVA FRONTERA'],
    'VALLE':['NACAOME','ALIANZA','AMAPALA','ARAMECINA','CARIDAD','GOASCORÁN','LANGUE','SAN FRANCISCO DE CORAY','SAN LORENZO'],
    'YORO':['YORO','ARENAL','EL NEGRITO','EL PROGRESO','JOCÓN','MORAZÁN','OLANCHITO','SANTA RITA','SULACO','VICTORIA','YORITO']
}

#años= ['2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021']

años= ['2016', '2017', '2020']


for año in años: 
    print(año)
    for depto in Deptos:
        for mun in municipios[depto]:
            print(año,depto,mun)
            for delito in delitos: 

                print(año,depto,mun,delito)

                

                #escoge el departamento
                element = wait.until(EC.element_to_be_clickable((By.ID, 'dep_cod')))
                element.send_keys(depto)

                #escoge el año de referencia
                click_until_interactable( By.ID,'anio')
                element = wait.until(EC.element_to_be_clickable((By.ID, 'anio')))
                element.send_keys(año)

                #escoge el municipio
                click_until_interactable( By.ID,'mun_cod')
                element = wait.until(EC.element_to_be_clickable((By.ID, 'mun_cod')))
                element.send_keys(mun)

                #escoge la categoria de las estadisticas
                click_until_interactable( By.ID,'incact_cod')
                element = wait.until(EC.element_to_be_clickable((By.ID, 'incact_cod')))
                element.send_keys(delito)

                driver.execute_script("window.scrollTo(0,0)")

                # va y escoge la fecha de inicio 
                click_until_interactable( By.ID,'fch_inicio')
                element = wait.until(EC.element_to_be_clickable((By.ID, 'fch_inicio')))
                element.click()
                click_until_interactable(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]')
                driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]').click()
                driver.find_element(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]').send_keys('Ene')
                dias = driver.find_elements(By.CLASS_NAME, 'ui-state-default')
                for i in dias:
                    if i.text == "1":
                        i.click()


                driver.execute_script("window.scrollTo(0,0)")

                # va y escoge la fecha final 
                click_until_interactable( By.ID,'fch_fin')
                element = wait.until(EC.element_to_be_clickable((By.ID, 'fch_fin')))
                element.click()
                click_until_interactable(By.XPATH,'//*[@id="ui-datepicker-div"]/div/div/select[1]')
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
                    print(año,depto,mun,delito,"sin registros")
                    df = pd.DataFrame(data={'Depto': [depto],'Mun':[mun], 'Año':año ,'Tipo Muerte': delito, 'Edad0_5':0,'Edad6_10':0,'Edad11_14':0,'Edad15_18':0})
                    SEPOL = pd.concat([SEPOL, df])

                except NoSuchElementException:

                    # va a la tabla 
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabs-two"]/ul/li[3]/a')))
                    element.send_keys("\n")


                    tabla = driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table').text

                    Edad0_5=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[3]/td[2]').text)
                    Edad6_10=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[4]/td[2]').text)
                    Edad11_14=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[5]/td[2]').text)
                    Edad15_18=int(driver.find_element(By.XPATH,'//*[@id="tab-two3"]/div/table/tbody/tr[6]/td[2]').text)

                    df = pd.DataFrame(data={'Depto': [depto],'Mun':[mun], 'Año':año ,'Tipo Muerte': delito, 'Edad0_5':Edad0_5,'Edad6_10':Edad6_10,'Edad11_14':Edad11_14,'Edad15_18':Edad15_18,'-18':(Edad0_5+Edad6_10+Edad11_14+Edad15_18)})

                    SEPOL = pd.concat([SEPOL, df])
                    SEPOL.to_excel("/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos/SEPOL.xlsx", sheet_name="SEPOL",index=False)


                print(año,depto,mun,delito,"hecho")

                


driver.quit()
SEPOL.to_excel("/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos/SEPO_total.xlsx", sheet_name="SEPOL",index=False)




