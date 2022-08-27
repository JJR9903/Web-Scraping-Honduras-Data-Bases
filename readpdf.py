#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 11:07:38 2022

@author: JuanJose

conda update anaconda
conda install spyder=5.2.2
"""
#!pip install tabula-py

import pandas as pd   
import tabula
import re


def resub(x):
    return re.sub(',','',x)

# leer la tabla de pdf

path = "/Users/JuanJose/Desktop/Poblacion INE/"
pdf_path = path+"Tomo 10 Atlantida.pdf"
df = tabula.io.read_pdf(input_path=pdf_path,pages='3',stream=True,lattice=False,pandas_options={'header': None})[0]

#sacar la tabla especifica 
df1=df[0]

# hacer cualquier operación necesaria 
df1['Valor']=df.iloc[:,1].sum()
df1['Año']=2012
df1=df1[[0,'Valor','Año']]
df1=df1.iloc[5:27,  [0,1,2,3,5]]


# exportar la tabla a excel 
df1.to_excel("/Users/JuanJose/Desktop/ENDESA 2011-12 Provisional.xlsx")





# info de población de niñez total, urbana y rural por año y rango etario 
años = {2013:3,2014:5,2015:7,2016:9,2017:11,2018:13,2019:15,2020:17,2021:19,2022:21}
Pob=pd.DataFrame(columns=["Año","Depto","Total", "Urbana", "Rural", "0-4 Años", "5-9 Años", "10-14 Años", "15-19 Años"],index=años.keys())
Poblacion=pd.DataFrame()

Deptos = ["Atlantida","Comayagua","El Paraiso","Intibuca","Lempira","Santa Barbara","Choluteca","Colon","Copan","Cortes","Francisco Morazan","Gracias a Dios","Islas de la Bahia","La Paz","Ocotepeque","Olancho","Valle","Yoro"]

for Depto in Deptos: 
    pdf_path = path+"Tomo 10 "+Depto+".pdf"
    url_pdf_path="https://www.ine.gob.hn/publicaciones/Proyecciones2030Dep/Tomo%2010%20"+Depto+".pdf"
    for k,v in años.items():
        print(Depto,k,v)
        df = tabula.io.read_pdf(input_path=pdf_path,pages=v,stream=True,lattice=False,pandas_options={'header': None})[0]
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
    

Poblacion.to_excel("/Users/JuanJose/Desktop/indicadores SIGADENAH.xlsx", sheet_name="Poblacion")

