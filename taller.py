# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import requests
import datetime

# Se consume el servicio REST para obtener el json con los datos
json_sismos = requests.get("https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime="+(datetime.datetime.now() + datetime.timedelta(hours=5)).strftime('%Y-%m-%d %H:%M:%S')).json()

#Convertimos el json a un diccionario
df_json_sismos = pd.DataFrame.from_dict(json_sismos["features"])

#Extraer propiedades
propiedades_sismos = df_json_sismos.properties

propiedades_sismos = propiedades_sismos.to_json()

df_sismos = pd.read_json(propiedades_sismos).transpose()

#Extraer coordenadas
coordenadas_sismos= df_json_sismos.geometry

coordenadas_sismos_json = coordenadas_sismos.to_json()

df_coordenadas = pd.read_json(coordenadas_sismos_json).transpose()

#Agregamos coordenadas a dataframe de sismos seleccionando la columna correspondiente
df_sismos = df_sismos.assign(coordinates=df_coordenadas.iloc[:,1])

#Convertir time epoch a date
df_sismos['time'] = pd.to_datetime(df_sismos['time'],unit='ms')

df_sismos.time = df_sismos.time - datetime.timedelta(hours=6)

#Exportamos las columnas que queremos
df_sismos.reset_index().to_csv('sismos.csv',columns=['place','mag','time','coordinates'],header=True,index=False)

