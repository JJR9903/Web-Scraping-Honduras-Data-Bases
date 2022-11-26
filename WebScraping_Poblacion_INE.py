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

python3  WebScraping_Poblacion_INE.py

#desactivar el ambiente virtual
deactivate
"""


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import Select
import re






chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")
chrome_options.headless = True
driver = webdriver.Chrome(executable_path='./chromedriver',options=chrome_options)
driver.get("http://181.115.7.199/binhnd/RpWebStats.exe/CrossTab?BASE=PROYPOB&ITEM=PROTOTANO&lang=ESP")
driver.maximize_window()
action = ActionChains(driver)
wait = WebDriverWait(driver, 5)

Poblacion_INE = pd.DataFrame(data={'Depto':"Depto",'Mun':"Mun",'Año':'Año','0':'0 años','1':'1 año','2':'2 años','3':'3 años','4':'4 años','5':'5 años','6':'6 años','7':'7 años','8':'8 años','9':'9 años','10':'10 años','11':'11 años','12':'12 años','13':'13 años','14':'14 años','15':'15 años','16':'16 años','17':'17 años','18':'18años'},index=[0])


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


Poblacion_INE = pd.DataFrame(columns=['Depto','Mun','Año','0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18'])




Deptos= ['ATLÁNTIDA', 'COLON', 'COMAYAGUA', 'COPAN', 'CORTES', 'CHOLUTECA', 'EL PARAÍSO', 'FRANCISCO MORAZÁN', 'GRACIAS A DIOS', 'INTIBUCÁ', 'ISLAS DE LA BAHÍA', 'LA PAZ', 'LEMPIRA', 'OCOTEPEQUE', 'OLANCHO', 'SANTA BÁRBARA', 'VALLE', 'YORO']

municipios= {
    'ATLÁNTIDA':{'LA CEIBA':"0101",'EL PORVENIR':"0102",'ESPARTA':"0103",'JUTIAPA':"0104",'LA MASICA':"0105",'SAN FRANCISCO':"0106",'TELA':"0107",'ARIZONA':"0108"},
    'COLON':{'TRUJILLO':'0201','BALFATE':'0202','IRIONA':'0203','LIMÓN':'0204','SABÁ':'0208','SANTA FE':'0205','SANTA ROSA DE AGUÁN':'0206','SONAGUERA':'0207','TOCOA':'0209','BONITO ORIENTAL':'0210'},
    'COMAYAGUA':{'COMAYAGUA':'0301','AJUTERIQUE':'0302','EL ROSARIO':'0303','ESQUÍAS':'0304','HUMUYA':'0305','LA LIBERTAD':'0306','LAMANÍ':'0307','LA TRINIDAD':'0308','LEJAMANÍ':'0309','MEÁMBAR':'0310','MINAS DE ORO':'0311','OJOS DE AGUA':'0312','SAN JERÓNIMO':'0312','SAN JOSÉ DE COMAYAGUA':'0314','SAN JOSE DEL POTRERO':'0315','SAN LUIS':'0316','SAN SEBASTIAN':'0317','SIGUATEPEQUE':'0318','VILLA DE SAN ANTONIO':'0319','LAS LAJAS':'0320','TAULABE':'0321'},
    'COPAN':{'SANTA ROSA DE COPÁN':'0401','CABAÑAS':'0402','CONCEPCIÓN':'0403','COPÁN RUINAS':'0404','CORQUÍN':'0405','CUCUYAGUA':'0406','DOLORES':'0407','DULCE NOMBRE':'0408','EL PARAÍSO':'0409','FLORIDA':'0410','LA JIGUA':'0411','LA UNIÓN':'0412','NUEVA ARCADIA':'0413','SAN AGUSTÍN':'0414','SAN ANTONIO':'0415','SAN JERÓNIMO':'0416','SAN JOSÉ':'0417','SAN JUAN DE OPOA':'0418','SAN NICOLÁS':'0419','SAN PEDRO DE COPÁN':'0420','SANTA RITA':'0421','TRINIDAD DE COPÁN':'0422','VERACRUZ':'0423'},
    'CORTES':{'SAN PEDRO SULA':'0501','CHOLOMA':'0502','OMOA':'0503','PIMIENTA':'0504','POTRERILLOS':'0505','PUERTO CORTÉS':'0506','SAN ANTONIO DE CORTÉS':'0507','SAN FRANCISCO DE YOJOA':'0508','SAN MANUEL':'0509','SANTA CRUZ DE YOJOA':'0510','VILLANUEVA':'0511','LA LIMA':'0512'},
    'CHOLUTECA':{'CHOLUTECA':'0601','APACILAGUA':'0602','CONCEPCIÓN DE MARIA':'0603','DUYURE':'0604','EL CORPUS':'0605','EL TRIUNFO':'0606','MARCOVIA':'0607','MOROLICA':'0608','NAMASIGUE':'0609','OROCUINA':'0610','PESPIRE':'0611','SAN ANTONIO DE FLORES':'0612','SAN ISIDRO':'0613','SAN JOSÉ':'0614','SAN MARCOS DE COLON':'0615','SANTA ANA DE YUSGUARE':'0616'},
    'EL PARAÍSO':{'YUSCARÁN':'0711','ALAUCA':'0702','DANLÍ':'0703','EL PARAÍSO':'0704','GÜINOPE':'0705','JACALEAPA':'0706','LIURE':'0707','MOROCELÍ':'0708','OROPOLÍ':'0709','POTRERILLOS':'0710','SAN ANTONIO DE FLORES':'0711','SAN LUCAS':'0712','SAN MATÍAS':'0713','SOLEDAD':'0714','TEUPASENTI':'0715','TEXIGUAT':'0716','VADO ANCHO':'0717','YAUYUPE':'0718','TROJES':'0719'},
    'FRANCISCO MORAZÁN':{'DISTRITO CENTRAL':'0801','ALUBAREN':'0802','CEDROS':'0813','CURARÉN':'0804','EL PORVENIR':'0805','GUAIMACA':'0806','LA LIBERTAD':'0807','LA VENTA':'0808','LEPATERIQUE':'0809','MARAITA':'0810','MARALE':'0811','NUEVA ARMENIA':'0812','OJOJONA':'0813','ORICA':'0814','REITOCA':'0815','SABANAGRANDE':'0816','SAN ANTONIO DE ORIENTE':'0817','SAN BUENAVENTURA':'0818','SAN IGNACIO':'0819','SAN JUAN DE FLORES':'0820','SAN MIGUELITO':'0821','SANTA ANA':'0822','SANTA LUCÍA':'0823','TALANGA':'0824','TATUMBLA':'0825','VALLE DE ANGELES':'0826','VILLA DE SAN FRANCISCO':'0827','VALLECILLO':'0828'},
    'GRACIAS A DIOS':{'PUERTO LEMPIRA':'0901','BRUS LAGUNA':'0902','AHUAS':'0904','JUAN FRANCISCO BULNES':'0903','VILLEDA MORALES':'0906','WAMPUSIRPI':'0905'},
    'INTIBUCÁ':{'LA ESPERANZA':'1001','CAMASCA':'1002','COLOMONCAGUA':'1003','CONCEPCIÓN':'1004','DOLORES':'1005','INTIBUCÁ':'1006','JESÚS DE OTORO':'1007','MAGDALENA':'1008','MASAGUARA':'1009','SAN ANTONIO':'1010','SAN ISIDRO':'1011','SAN JUAN':'1012','SAN MARCOS DE LA SIERRA':'1013','SAN MIGUELITO':'1014','SANTA LUCÍA':'1015','YAMARANGUILA':'1016','SAN FRANCISCO DE OPALACA':'1017'},
    'ISLAS DE LA BAHÍA':{'ROATÁN':'1101','GUANAJA':'1102','JOSÉ SANTOS GUARDIOLA':'1103','UTILA':'1104'},
    'LA PAZ':{'LA PAZ':'1201','AGUANQUETERIQUE':'1202','CABAÑAS':'1203','CANE':'1204','CHINACLA':'1205','GUAJIQUIRO':'1206','LAUTERIQUE':'1207','MARCALA':'1208','MERCEDES DE ORIENTE':'1209','OPATORO':'1210','SAN ANTONIO DEL NORTE':'1211','SAN JOSÉ':'1212','SAN JUAN':'1213','SAN PEDRO DE TUTULE':'1214','SANTA ANA':'1215','SANTA ELENA':'1216','SANTA MARÍA':'1217','SANTIAGO DE PURINGLA':'1218','YARULA':'1219'},    
    'LEMPIRA':{'GRACIAS':'1301','BELÉN':'1302','CANDELARIA':'1303','COLOLACA':'1304','ERANDIQUE':'1305','GUALCINCE':'1306','GUARITA':'1307','LA CAMPA':'1308','LA IGUALA':'1309','LAS FLORES':'1310','LA UNIÓN':'1311','LA VIRTUD':'1312','LEPAERA':'1313','MAPULACA':'1314','PIRAERA':'1315','SAN ANDRÉS':'1316','SAN FRANCISCO':'1317','SAN JUAN GUARITA':'1318','SAN MANUEL COLOHETE':'1319','SAN RAFAEL':'1320','SAN SEBASTIÁN':'1321','SANTA CRUZ':'1322','TALGUA':'1323','TAMBLA':'1324','TOMALÁ':'1325','VALLADOLID':'1326','VIRGINIA':'1327','SAN MARCOS DE CAIQUIN':'1328'},
    'OCOTEPEQUE':{'OCOTEPEQUE':'1401','BELÉN GUALCHO':'1402','CONCEPCIÓN':'1403','DOLORES MERENDÓN':'1404','FRATERNIDAD':'1405','LA ENCARNACIÓN':'1406','LA LABOR':'1407','LUCERNA':'1407','MERCEDES':'1409','SAN FERNANDO':'1410','SAN FRANCISCO DEL VALLE':'1411','SAN JORGE':'1412','SAN MARCOS':'1413','SANTA FE':'1414','SENSENTI':'1415','SINUAPA':'1416'},
    'OLANCHO':{'JUTICALPA':'1501','CAMPAMENTO':'1502','CATACAMAS':'1503','CONCORDIA':'1504','DULCE NOMBRE DE CULMÍ':'1505','EL ROSARIO':'1506','ESQUIPULAS DEL NORTE':'1507','GUALACO':'1508','GUARIZAMA':'1509','GUATA':'1510','GUAYAPE':'1511','JANO':'1512','LA UNIÓN':'1513','MANGULILE':'1514','MANTO':'1515','SALAMÁ':'1516','SAN ESTEBAN':'1517','SAN FRANCISCO DE BECERRA':'1518','SAN FRANCISCO DE LA PAZ':'1519','SANTA MARÍA DEL REAL':'1520','SILCA':'1521','YOCÓN':'1522','PATUCA':'1523'},
    'SANTA BÁRBARA':{'SANTA BÁRBARA':'1601','ARADA':'1602','ATIMA':'1603','AZACUALPA':'1604','CEGUACA':'1605','CONCEPCIÓN DEL NORTE':'1607','CONCEPCIÓN DEL SUR':'1608','CHINDA':'1609','EL NÍSPERO':'1610','GUALALA':'1611','ILAMA':'1612','MACUELIZO':'1613','NARANJITO':'1614','NUEVO CELILAC':'1615','PETOA':'1616','PROTECCIÓN':'1617','QUIMISTÁN':'1618','SAN FRANCISCO DE OJUERA':'1619','SAN JOSÉ DE COLINAS':'1606','SAN LUIS':'1620','SAN MARCOS':'1621','SAN NICOLÁS':'1622','SAN PEDRO ZACAPA':'1623','SAN VICENTE CENTENARIO':'1625','SANTA RITA':'1624','TRINIDAD':'1626','LAS VEGAS':'1627','NUEVA FRONTERA':'1628'},
    'VALLE':{'NACAOME':'1701','ALIANZA':'1702','AMAPALA':'1703','ARAMECINA':'1704','CARIDAD':'1705','GOASCORÁN':'1706','LANGUE':'1707','SAN FRANCISCO DE CORAY':'1708','SAN LORENZO':'1709'},
    'YORO':{'YORO':'1801','ARENAL':'1802','EL NEGRITO':'1803','EL PROGRESO':'1804','JOCÓN':'1805','MORAZÁN':'1806','OLANCHITO':'1807','SANTA RITA':'1808','SULACO':'1809','VICTORIA':'1810','YORITO':'1811'}
}

años= ['2016', '2020']

for año in años: 
    for depto in Deptos:
        for mun in municipios[depto]:
            
            print(mun)
            print(depto,mun,municipios[depto][mun])
            
            
            filtro = "MUNIC.REDCODEN =" + municipios[depto][mun] + " AND PROYEC.AN =" + año +" AND (PROYEC.EDAD>=0 AND PROYEC.EDAD<=18)"
            print(filtro)

            element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="redInput"]/form/div[2]/table/tbody/tr[1]/td[2]/select')))
            select = Select(driver.find_element(By.XPATH,'//*[@id="redInput"]/form/div[2]/table/tbody/tr[1]/td[2]/select'))
            select.select_by_value('PROYEC.EDAD')


            element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="redInput"]/form/div[3]/table/tbody/tr[4]/td[2]/textarea')))
            element.send_keys(filtro)


            element = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="Submit"]')))
            element.click()

            wait.until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="redStatusDialog"]')))

            E0 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[17]/td[3]').text
            E1 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[18]/td[3]').text
            E2 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[19]/td[3]').text
            E3 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[20]/td[3]').text
            E4 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[21]/td[3]').text
            E5 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[22]/td[3]').text
            E6 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[23]/td[3]').text
            E7 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[24]/td[3]').text
            E8 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[25]/td[3]').text
            E9 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[26]/td[3]').text
            E10 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[27]/td[3]').text
            E11 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[28]/td[3]').text
            E12 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[29]/td[3]').text
            E13 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[30]/td[3]').text
            E14 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[31]/td[3]').text
            E15 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[32]/td[3]').text
            E16 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[33]/td[3]').text
            E17 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[34]/td[3]').text
            E18 = driver.find_element(By.XPATH,'//*[@id="tab-output"]/div/div[1]/table/tbody/tr[35]/td[3]').text  


            Pobl = pd.DataFrame(data={'Depto':depto,'Mun':mun,'Año':año,'0':E0,'1':E1,'2':E2,'3':E3,'4':E4,'5':E5,'6':E6,'7':E7,'8':E8,'9':E9,'10':E10,'11':E11,'12':E12,'13':E13,'14':E14,'15':E15,'16':E16,'17':E17,'18':E18},index=[0])
            num_cols = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']

            for i in num_cols:
                Pobl[i] = Pobl[i].str.replace(',', '')

            Poblacion_INE= pd.concat([Poblacion_INE,Pobl])
            Poblacion_INE.to_excel("/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos/Poblacion_NNA_INE.xlsx", sheet_name="Poblacion_NNA_INE",index=False)

            driver.refresh()
            
