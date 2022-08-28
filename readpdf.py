#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 11:07:38 2022

@author: JuanJose
"""


import pandas as pd   
import numpy as np
import tabula
import re
import os


def resub(x):
    '''
    función que toma a x y le quita la coma (,) de los miles y millones para poder convertir el str en int
    '''
    return re.sub(',','',x)

# leer la tabla de pdf
# tabula.io.read_pdf(input_path='pdf path', pages='# page to read', stream='False', lattice='False', pandas_options='{'header':None}',area={top,left,bottom,rigth}))

os.chdir('/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos')



#### ENDESA 2011-12
ENDESA_2011_URL= "https://www.ine.gob.hn/publicaciones/endesa/Honduras-ENDESA-2011-2012.pdf"
ENDESA_2011=pd.DataFrame(columns=['Depto','Año'])
ENDESA_2011['Año']=2011
ENDESA_2011['Depto']=['Atlantida','Colon','Comayagua','Copan','Cortes','San Pedro Sula','Resto Cortes','Choluteca','El Paraiso','Francisco Morazan','Distrito Central','Resto Fco. Morazan','Gracias a Dios','Intibuca','Islas de la Bahia','La Paz', 'Lempira','Ocotepeque','Olancho','Santa Barbara','Valle','Yoro']


# diccionario que especifica para cada variable a sacar del pdf, el nombre de la variable dict.key, la pagína en que se encuentra la tabla, las columnas que necesitan sumar para la variable, y el area de la página pdf en la que se encuentra la tabla 
tablas = {'Aguas Mejoradas':{'pag':57,'columnas':[1,2,3,4,5,6,10],'area':(189.09,53.48,368.73,442.16)},
          'Servicio Sanitario':{'pag':58,'columnas':[1,2,4,5,6],'area':(464.49,51.43,645.48,335.36)},
          'Lavado de manos':{'pag':67,'columnas':[3],'area':(222.59,60.88,401.01,253.3)},
          'NNA de crianza':{'pag':73,'columnas':[13],'area':(322.23,54.19,501.17,526.85)},
          'NNA huerfanos':{'pag':73,'columnas':[12],'area':(322.23,54.19,501.17,526.85)},
          'Certificado de Nacimiento':{'pag':74,'columnas':[1],'area':(435.21,133.25,612.43,397.32)},
          'Registro de Nacimiento': {'pag':74,'columnas':[3],'area':(435.21,133.25,612.43,397.32)},
          'Embarazo Adolescente (Muejeres)': {'pag':152,'columnas':[3],'area':(408.15,301.54,585.07,514.62)},
          'Mortalidad NeoNatal': {'pag':209,'columnas':[1],'area':(199.5,141.98,389.53,456.39)},
          'Mortalidad Post-Neonatal': {'pag':209,'columnas':[2],'area':(199.5,141.98,389.53,456.39)},
          'Mortalidad Infantil': {'pag':209,'columnas':[3],'area':(199.5,141.98,389.53,456.39)},
          'Mortalidad 1-4 años': {'pag':209,'columnas':[4],'area':(199.5,141.98,389.53,456.39)},
          'Mortalidad en la Niñiez': {'pag':209,'columnas':[5],'area':(199.5,141.98,389.53,456.39)},
          'Atencion Prenatal':{'pag':223,'columnas':[1,2,3,4],'area':(352.61,85.59,521.94,467.78)},
          'Atencion Prenatal (Personal de Salud)':{'pag':223,'columnas':[7],'area':(352.61,85.59,521.94,467.78)},
          'Parto en Esatablecimiento de Salud': {'pag':230,'columnas':[6],'area':(347.22,106.73,525.18,453.33)},
          'Parto Atendido por Profesional': {'pag':232,'columnas':[8],'area':(333.94,49.06,503.19,462.88)},
          'Revision Post-Natal para la madre': {'pag':236,'columnas':[8],'area':(335.79,67.51,500.79,491.15)},
          'Revision (por profesional) Post-Natal para la madre': {'pag':237,'columnas':[7],'area':(334.24,84.73,503.82,486.81)},
          'Revision Post-Natal para el Bebe': {'pag':239,'columnas':[8],'area':(342,67.12,510,490.77)},
          'Revision (por profesional) Post-Natal para el Bebe': {'pag':241,'columnas':[7],'area':(319,76.79,486.67,477.94)},
          #'Menor tamaño al nacer': {'pag':251,'columnas':[1,2],'area':(356,59.87,532.99,469.49)},
          'Pesados al Nacer': {'pag':251,'columnas':[6],'area':(356,59.87,532.99,469.49)},
          'Peso menos de 2.5kg': {'pag':251,'columnas':[8],'area':(356,59.87,532.99,469.49)},
          'NNA de 1 año con Vacunas obligatorias': {'pag':254,'columnas':[9],'area':(259.19,76.1,435.76,488.65)},
          'NNA de 1 año con Carnet de Vacunacion': {'pag':254,'columnas':[11],'area':(259.19,76.1,435.76,488.65)},
          'Prevalencia de Neumonia': {'pag':259,'columnas':[1],'area':(372,97,547.29,237.88)},
          'Prevalencia de Fiebre': {'pag':262,'columnas':[1],'area':(299,88.24,475.3,218.19)},
          'Prevalencia de Diarrea': {'pag':265,'columnas':[1],'area':(299.66,313.31,476.29,443.87)},
          'Lactancia Materna': {'pag':278,'columnas':[1],'area':(349.68,90.41,517.1,225.09)},
          'Lactancia Materna Exclusiva': {'pag':281,'columnas':[2],'area':(244,301.14,412.21,500.66)},
          'Prevalencia de Anemia': {'pag':297,'columnas':[1],'area':(312,144.8,479.55,283.01)},
          'Baja Talla para la Edad': {'pag':304,'columnas':[2],'area':(204.3,76.65,372.92,479.36)},
          'Bajo Peso para la Talla': {'pag':304,'columnas':[4],'area':(204.3,76.65,372.92,479.36)},
          'Sobrepeso/Obesidad': {'pag':304,'columnas':[5],'area':(204.3,76.65,372.92,479.36)},
          'Bajo Peso para la Edad': {'pag':304,'columnas':[7],'area':(204.3,76.65,372.92,479.36)},
          'Prueva VIH durante Atencion Pre-Natal': {'pag':362,'columnas':[6],'area':(333,59.06,500.71,434.15)},
          'Assitencia a Educacion Temprana':  {'pag':449,'columnas':[1],'area':(358,75.83,706.68,228.9)},
          'NNA con Atencion inadecuada': {'pag':455,'columnas':[3],'area':(285.14,130.39,462.47,415.03)},
          'Indice de Desarrollo Infantil Temprano': {'pag':459,'columnas':[5],'area':(383.18,113.36,558.95,438.4)}
          }

#sacar la tabla especifica 
for v in tablas.keys():
    print(v)
    df = tabula.io.read_pdf(input_path=ENDESA_2011_URL,pages=tablas[v]['pag'],stream=True,lattice=False,pandas_options={'header': None},area=tablas[v]['area'])[0]
    ENDESA_2011[v]=df.iloc[:,tablas[v]['columnas']].sum(axis=1)

ENDESA_2011['Año']=2011

ENDESA_2011.loc[ENDESA_2011['Depto']=="Islas de la Bahia",'Lactancia Materna Exclusiva']=np.nan
ENDESA_2011['Lactancia Materna Exclusiva']=pd.to_numeric(ENDESA_2011['Lactancia Materna Exclusiva'])

# exportar la tabla a excel 
ENDESA_2011.to_excel("ENDESA 2011-12 NNA.xlsx", sheet_name="ENDESA 2011-12 ",index=False)











#### ENDESA 2019
ENDESA_2019_os=os.listdir('/Users/JuanJose/Library/CloudStorage/GoogleDrive-j.rincon@econometria.com/Mi unidad/SIGADENAH/Bases de Datos/ENDESA MICS 2019/Excel')
ENDESA_2019=pd.DataFrame(columns=['Depto','Año'])
ENDESA_2019['Año']=2019
ENDESA_2019['Depto']=['Atlantida','Colon','Comayagua','Copan','Cortes','San Pedro Sula','Resto Cortes','Choluteca','El Paraiso','Francisco Morazan','Distrito Central','Resto Fco. Morazan','Gracias a Dios','Intibuca','Islas de la Bahia','La Paz', 'Lempira','Ocotepeque','Olancho','Santa Barbara','Valle','Yoro']


# diccionario que especifica para cada variable a sacar del pdf, el nombre de la variable dict.key, la pagína en que se encuentra la tabla, las columnas que necesitan sumar para la variable, y el area de la página pdf en la que se encuentra la tabla 
tablas = {'Aguas Mejoradas': {'xlsx':ENDESA_2019_os[10],'sheet_name':'1.1','usecols':"A,T",'skiprows':12},
          'Servicio Sanitario': {'xlsx':ENDESA_2019_os[10],'sheet_name':'3.1','usecols':"A,N",'skiprows':12},
          'Lavado de manos': {'xlsx':ENDESA_2019_os[10],'sheet_name':'2.1','usecols':"A,L",'skiprows':12},
          'NNA de crianza': {'xlsx':ENDESA_2019_os[5],'sheet_name':'11.1','usecols':"A,P",'skiprows':13},
          'NNA huerfanos': {'xlsx':ENDESA_2019_os[5],'sheet_name':'11.1','usecols':"A,C,D,F,I,L",'skiprows':13},
          'Certificado de Nacimiento': {'xlsx':ENDESA_2019_os[2],'sheet_name':'1.1','usecols':"A,B,C",'skiprows':14},
          'Registro de Nacimiento': {'xlsx':ENDESA_2019_os[2],'sheet_name':'1.1','usecols':"A,F",'skiprows':14},
          'Embarazo Adolescente (Muejeres)': {'xlsx':ENDESA_2019_os[9],'sheet_name':'2.2W','usecols':"A,D,E",'skiprows':10},
          'Mortalidad NeoNatal': {'xlsx':ENDESA_2019_os[4],'sheet_name':'2 (BH)','usecols':"A,B",'skiprows':9},
          'Mortalidad Post-Neonatal': {'xlsx':ENDESA_2019_os[4],'sheet_name':'2 (BH)','usecols':"A,C",'skiprows':9},
          'Mortalidad Infantil': {'xlsx':ENDESA_2019_os[4],'sheet_name':'2 (BH)','usecols':"A,D",'skiprows':9},
          'Mortalidad 1-4 años': {'xlsx':ENDESA_2019_os[4],'sheet_name':'2 (BH)','usecols':"A,E",'skiprows':9},
          'Mortalidad en la Niñiez': {'xlsx':ENDESA_2019_os[4],'sheet_name':'2 (BH)','usecols':"A,F",'skiprows':9},
          'Atencion Prenatal': {'xlsx':ENDESA_2019_os[9],'sheet_name':'4.1','usecols':"A,B,C,D,E,F",'skiprows':10},
          'Atencion Prenatal (Personal de Salud)': {'xlsx':ENDESA_2019_os[9],'sheet_name':'4.1','usecols':"A,I",'skiprows':10},
          'Parto en Esatablecimiento de Salud': {'xlsx':ENDESA_2019_os[9],'sheet_name':'6.1','usecols':"A,H",'skiprows':11},
          'Parto Atendido por Profesional': {'xlsx':ENDESA_2019_os[9],'sheet_name':'6.2','usecols':"A,L",'skiprows':11},
          'Revision Post-Natal para la madre': {'xlsx':ENDESA_2019_os[9],'sheet_name':'8.7','usecols':"A,K",'skiprows':13},
          'Revision (por profesional) Post-Natal para la madre': {'xlsx':ENDESA_2019_os[9],'sheet_name':'8.8','usecols':"A,H,I,J",'skiprows':13},
          'Revision Post-Natal para el Bebe': {'xlsx':ENDESA_2019_os[9],'sheet_name':'8.2','usecols':"A,K",'skiprows':13},
          'Revision (por profesional) Post-Natal para el Bebe': {'xlsx':ENDESA_2019_os[9],'sheet_name':'8.3','usecols':"A,H,I,J",'skiprows':13},
          #'Menor tamaño al nacer': ,
          'Pesados al Nacer': {'xlsx':ENDESA_2019_os[9],'sheet_name':'7.1','usecols':"A,D",'skiprows':10},
          'Peso menos de 2.5kg': {'xlsx':ENDESA_2019_os[9],'sheet_name':'7.1','usecols':"A,H",'skiprows':10},
          'NNA de 1 año con Vacunas obligatorias': {'xlsx':ENDESA_2019_os[1],'sheet_name':'1.2','usecols':"A,T",'skiprows':14},
          'NNA de 1 año con Carnet de Vacunacion': {'xlsx':ENDESA_2019_os[1],'sheet_name':'1.2','usecols':"A,W",'skiprows':14},
          'Prevalencia de Neumonia': {'xlsx':ENDESA_2019_os[1],'sheet_name':'2.1','usecols':"A,C",'skiprows':13},
          'Prevalencia de Fiebre': {'xlsx':ENDESA_2019_os[1],'sheet_name':'2.1','usecols':"A,D",'skiprows':13},
          'Prevalencia de Diarrea': {'xlsx':ENDESA_2019_os[1],'sheet_name':'2.1','usecols':"A,B",'skiprows':13},
          'Lactancia Materna': {'xlsx':ENDESA_2019_os[1],'sheet_name':'7.1','usecols':"A,B",'skiprows':10},
          'Lactancia Materna Exclusiva': {'xlsx':ENDESA_2019_os[1],'sheet_name':'7.4','usecols':"A,D",'skiprows':13},
          'Prevalencia de Anemia': {'xlsx':ENDESA_2019_os[1],'sheet_name':'12.1','usecols':"A,B",'skiprows':16},
          'Baja Talla para la Edad': {'xlsx':ENDESA_2019_os[1],'sheet_name':'8.1','usecols':"A,F",'skiprows':15},
          'Bajo Peso para la Talla': {'xlsx':ENDESA_2019_os[1],'sheet_name':'8.1','usecols':"A,J",'skiprows':15},
          'Sobrepeso/Obesidad': {'xlsx':ENDESA_2019_os[1],'sheet_name':'8.1','usecols':"A,M",'skiprows':15},
          'Bajo Peso para la Edad': {'xlsx':ENDESA_2019_os[1],'sheet_name':'8.1','usecols':"A,B",'skiprows':15},
          'Prueva VIH durante Atencion Pre-Natal': {'xlsx':ENDESA_2019_os[9],'sheet_name':'11.5','usecols':"A,E",'skiprows':10},
          'Assitencia a Educacion Temprana': {'xlsx':ENDESA_2019_os[8],'sheet_name':'1.1','usecols':"A,B",'skiprows':12},
          'NNA con Atencion inadecuada': {'xlsx':ENDESA_2019_os[1],'sheet_name':'10.3','usecols':"A,D",'skiprows':13},
          'Indice de Desarrollo Infantil Temprano': {'xlsx':ENDESA_2019_os[1],'sheet_name':'11.1','usecols':"A,F",'skiprows':13}
          }



for v in tablas.keys():
    df=pd.read_excel(io="ENDESA MICS 2019/Excel/"+tablas[v]['xlsx'],sheet_name=tablas[v]['sheet_name'],usecols=tablas[v]['usecols'],skiprows=tablas[v]['skiprows'],nrows=22)
    print(v)
    ENDESA_2019[v]=df.drop(['Departamento'],axis=1).sum(axis=1)
    
ENDESA_2019['Año']=2019

# exportar la tabla a excel 
ENDESA_2019.to_excel("ENDESA 2019 NNA.xlsx", sheet_name="ENDESA 2019 ",index=False)










#PROYECCIONES POBLACIONALES 

# info de población de niñez total, urbana y rural por año y rango etario 
años = {2013:3,2014:5,2015:7,2016:9,2017:11,2018:13,2019:15,2020:17,2021:19,2022:21}
Pob=pd.DataFrame(columns=["Año","Depto","Total", "Urbana", "Rural", "0-4 Años", "5-9 Años", "10-14 Años", "15-19 Años"],index=años.keys())
Poblacion=pd.DataFrame()

Deptos = ["Atlantida","Comayagua","El Paraiso","Intibuca","Lempira","Santa Barbara","Choluteca","Colon","Copan","Cortes","Francisco Morazan","Gracias a Dios","Islas de la Bahia","La Paz","Ocotepeque","Olancho","Valle","Yoro"]

for Depto in Deptos: 
    url_pdf_path="https://www.ine.gob.hn/publicaciones/Proyecciones2030Dep/Tomo%2010%20"+Depto+".pdf"
    for k,v in años.items():
        print(Depto,k,v)
        df = tabula.io.read_pdf(input_path=url_pdf_path,pages=v,stream=True,lattice=False,pandas_options={'header': None})[0]
        total=pd.DataFrame(df.iloc[3,]).reset_index(drop=True)
        total=total.applymap(resub)
        total=total.drop([0])
        total=total[3].astype(int)
        df=df.iloc[4:8,]
        df=df.applymap(resub)
        for i in range(1,10):
            df[i]=df[i].astype(int)
        Pob.loc[k,"Año"]=k
        Pob.loc[k,"Depto"]=Depto
        Pob.loc[k,"Total"]=df.iloc[:,1].sum()
        Pob.loc[k,"Urbana"]=df.iloc[:,4].sum()
        Pob.loc[k,"Rural"]=df.iloc[:,7].sum()
        Pob.loc[k,"0-4 Años"]=df.iloc[0,1]
        Pob.loc[k,"5-9 Años"]=df.iloc[1,1]
        Pob.loc[k,"10-14 Años"]=df.iloc[2,1]
        Pob.loc[k,"15-19 Años"]=df.iloc[3,1]
        Pob.loc[k,"% Total"]=df.iloc[:,1].sum()/total[1]
        Pob.loc[k,"% Urbana"]=df.iloc[:,4].sum()/total[4]
        Pob.loc[k,"% Rural"]=df.iloc[:,7].sum()/total[7]
        Pob.loc[k,"% 0-4 Años"]=df.iloc[0,1]/total[1]
        Pob.loc[k,"% 5-9 Años"]=df.iloc[1,1]/total[1]
        Pob.loc[k,"% 10-14 Años"]=df.iloc[2,1]/total[1]
        Pob.loc[k,"%15-19 Años"]=df.iloc[3,1]/total[1]
    Poblacion=pd.concat([Poblacion, Pob], ignore_index=True)
    

Poblacion.to_excel("Proyecciones Poblacionales NNA Honduras .xlsx", sheet_name="Poblacion",index=False)

