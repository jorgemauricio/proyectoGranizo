#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite el procesamiento
# de datos de precipitación de la NASA
# Author: Jorge Mauricio
# Email: jorge.ernesto.mauricio@gmail.com
# Date: 2018-02-01
# Version: 1.0
#######################################
Created on Mon Jul 17 16:17:25 2017
@author: jorgemauricio
"""
# librerias
import pandas as pd
import os
import math
import numpy as np

# Programa principal
def main():
    # limpiar la terminal
    os.system('clear')

    # lista de frames
    frames = []

    # path de archivos
    # Linux path = "/home/jorge/Documents/Research/proyectoGranizo"
    path = "/home/jorge/Documents/Research/proyectoGranizo"

    # nombre del archivo
    nombreTemporalArchivo = "{}/data/data_wrf_area_influencia.csv".format(path)

    # leer csv
    data = pd.read_csv(nombreTemporalArchivo)

    data["areaInfluencia"] = data["areaInfluencia"] / 21.16

    # iniciar con el procesamiento
    for nombre in data["Nombre"].unique():
        # clasificar la información por nombre
        dataTemp = data.loc[data["Nombre"] == nombre]

        # organizar la información por listaDeFechas
        dataTemp = dataTemp.sort_values(by=["Year","Month","Day","Hour"])

        # generar hora
        # dataTemp["Hora"] = dataTemp.apply(lambda x: generarHora(x["Hour"]), axis=1)

        # genear fecha agrupada
        dataTemp["Fecha"] = dataTemp.apply(lambda x: generarFecha(x["Year"], x["Month"], x["Day"], x["Hora_Formato"]), axis=1)

        # convertir fecha de objeto a datetime
        dataTemp['Fecha'] = dataTemp['Fecha'].astype('datetime64[ns]')

        # ordenar por fecha
        dataTemp = dataTemp.sort_values(by="Fecha")

        # print
        #print(dataTemp.head(30))

        # crear columna de diferencia tiempo previo
        dataTemp["diff_previa"] = abs(dataTemp["areaInfluencia"] - dataTemp["areaInfluencia"].shift(-1))

        # crear columna de diferencia tiempo posterior
        dataTemp["diff_posterior"] = abs(dataTemp["areaInfluencia"] - dataTemp["areaInfluencia"].shift(1))

        # crear columna de siguiente valor
        dataTemp["areaInfluencia_posterior_1"] = dataTemp["areaInfluencia"].shift(1)

        # crear columna de siguiente valor
        dataTemp["areaInfluencia_posterior_2"] = dataTemp["areaInfluencia"].shift(2)

        # generar rango previo de diff
        dataTemp["Rango_previo"] = dataTemp.apply(lambda x: generarRangoPrevio(x["diff_previa"]), axis=1)

        # generar rango posterios de diff
        dataTemp["Rango_posterior"] = dataTemp.apply(lambda x: generarRangoPosterior(x["diff_posterior"]), axis=1)

        # generar validación de evento en tiempo
        dataTemp["validacionEvento"] = dataTemp.apply(lambda x: validacionSeguimiento(x["areaInfluencia"], x["areaInfluencia_posterior_1"], x["areaInfluencia_posterior_2"]), axis=1)

        # eliminar datos nulos
        dataTemp = dataTemp.fillna(value=0)

        # evitar columnas ajenas
        dataTemp = dataTemp[['Canon', 'Estado', 'Nombre', 'Long', 'Lat', 'Year', 'Month', 'Day', 'Hour', 'RainWRF', 'areaInfluencia', 'areaInfluencia_posterior_1', 'areaInfluencia_posterior_2', 'diff_previa', 'diff_posterior', 'Rango_previo', 'Rango_posterior', 'validacionEvento', 'Fecha', 'Hora_Formato']]

        # agregar df temporal a frames
        frames.append(dataTemp)

        # procesamiento de {}
        print("procesamiento de:", nombre)

    # generar un solo archivo
    data = pd.concat(frames)

    # generar variables descriptivas
    for rango in data["Rango_previo"].unique():
        data[rango] = [1 if x == rango else 0 for x in data["Rango_previo"]]

    # guardar archivo a CSV
    nombreArchivoFinal = "{}/data/Resultado_wrf_area_influencia_3.csv".format(path)
    data.to_csv(nombreArchivoFinal, index=False)

def generarRangoPrevio(valor):
    if valor < 1:
        return "0pre"
    if valor >= 1 and valor <= 5:
        return "1-5pre"
    if valor > 5 and valor <= 10:
        return "5-10pre"
    if valor > 10 and valor <= 15:
        return "10-15pre"
    if valor > 15 and valor <= 20:
        return "15-20pre"
    if valor > 20 and valor <= 25:
        return "20-25pre"
    if valor > 25 and valor <= 30:
        return "25-30pre"
    if valor > 30:
        return ">30pre"

def generarRangoPosterior(valor):
    if valor < 1:
        return "0post"
    if valor >= 1 and valor <= 5:
        return "1-5post"
    if valor > 5 and valor <= 10:
        return "5-10post"
    if valor > 10 and valor <= 15:
        return "10-15post"
    if valor > 15 and valor <= 20:
        return "15-20post"
    if valor > 20 and valor <= 25:
        return "20-25post"
    if valor > 25 and valor <= 30:
        return "25-30post"
    if valor > 30:
        return ">30post"

def validacionSeguimiento(valorActual, valorPost, valorPost2):
    if valorActual > 20 and valorPost == 0 and valorPost2 == 0:
        return 1
    else:
        return 0

# def generarFecha(y,m,d,h):
#     if h == 0:
#         return "{}-{}-{} 0000".format(y,complementarValor(m),complementarValor(d),h)
#     if h < 100:
#         return "{}-{}-{} 00{}".format(y,complementarValor(m),complementarValor(d),h)
#     if h < 1000:
#         return "{}-{}-{} 0{}".format(y,complementarValor(m),complementarValor(d),h)
#     if h < 10000:
#         return "{}-{}-{} {}".format(y,complementarValor(m),complementarValor(d),h)
#
# def complementarValor(v):
#     if v < 10:
#         return "0{}".format(v)
#     else:
#         return "{}".format(v)

def generarFecha(y,m,d,h):
        return "{}-{}-{} {}".format(y,complementarValor(m),complementarValor(d),h)

def complementarValor(v):
    if v < 10:
        return "0{}".format(v)
    else:
        return "{}".format(v)

def generarHora(h):
    hour = int(h / 60)
    if hour < 10:
        hour = "0{}".format(hour)
    minutes = h % 60
    if minutes < 10:
        minutes = "0{}".format(minutes)
    return "{}:{}".format(hour, minutes)

if __name__ == '__main__':
    main()
