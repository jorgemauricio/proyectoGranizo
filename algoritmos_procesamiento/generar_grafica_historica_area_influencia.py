#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite crear gráfica histórica
# a partir de datos de precipitación de la NASA
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
import matplotlib.pyplot as plt

# Programa principal
def main():
    # limpiar la terminal
    os.system('clear')

    # path de archivos
    # Linux path = "/home/jorge/Documents/Research/proyectoGranizo"
    path = "/home/jorge/Documents/Research/proyectoGranizo"

    # nombre del archivo
    nombreTemporalArchivo = "{}/data/data_nasa_area_influencia.csv".format(path)

    # leer csv
    data = pd.read_csv(nombreTemporalArchivo)

    # iniciar con el procesamiento
    for i in data["Nombre"].unique():
        # acotar información por cañon
        dataTemp = data.loc[data["Nombre"] == i]

        # generar formato horario
        dataTemp["Hora"] = dataTemp.apply(lambda x: generarHora(x["Hour"]), axis=1)
        dataTemp["Fecha"] = dataTemp.apply(lambda x: generarFecha(x["Year"], x["Month"], x["Day"], x["Hora"]), axis=1)
        dataTemp['Fecha'] = dataTemp['Fecha'].astype('datetime64[ns]')
        dataTemp = dataTemp.sort_values(by="Fecha")

        dataTemp["areaInfluencia2"] = dataTemp["areaInfluencia"] / 21.26
        dataTemp.index = dataTemp["Fecha"]
        dataTemp.index = pd.to_datetime(dataTemp.index)

        #iniciar gráfica
        plt.clf()

        # configurar tamaño de gráfica
        fig = plt.figure(figsize=(50,5))
        ax = fig.add_subplot(111)

        # obtener x, y , e
        x = np.array(dataTemp.index)
        y = np.array(dataTemp["areaInfluencia2"])

        # configurar línea
        line, = ax.plot(x, y, lw=2)

        # generar títulos
        tituloGrafica = "CAÑON ANTIGRANIZO: {}".format(i)

        # configurar títulos
        ax.set_xlabel("FECHA")
        ax.set_ylabel("PP (mm)")
        ax.set_title(tituloGrafica)

        # guardar gráfica
        nombreTemporalGrafica = "data/graphs/{}_historica_af.png".format(i)
        plt.savefig(nombreTemporalGrafica, dpi=600)

        #print
        print("Graph: {}".format(i))

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

# declarar función main
if __name__ == '__main__':
    main()
