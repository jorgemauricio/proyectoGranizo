#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite crear gráficas a partir
# de datos de precipitación del WRF
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

    # número de prueba
    prueba = 1

    # nombre del archivo generado en procesamineto_datos_wrf.py
    nombreTemporalArchivo = "{}/data/Resultado_wrf_{}.csv".format(path, prueba)

    # leer csv
    data = pd.read_csv(nombreTemporalArchivo)

    # datos del 2014 al 2017
    data = data.loc[(data["Year"] >= 2014) & (data["Year"] <= 2017)]

    # generar dataFrame para graficas
    dataEventos = data[data["validacionEvento"] == 1]

    # iniciar con el procesamiento
    for i in range(0, dataEventos["Nombre"].count()):
        # generar variables para la clasificación de información
        # Nombre
        nombreEstacion = dataEventos.iloc[i]["Nombre"]
        # Año
        anio = dataEventos.iloc[i]["Year"]
        # Mes
        mes = dataEventos.iloc[i]["Month"]
        # Día
        dia = dataEventos.iloc[i]["Day"]

        # generar el dataFrame para procesamiento generar la gráfica
        dataGrafica = data[(data["Year"] == anio) & (data["Month"] == mes) & (data["Day"] == dia) & (data["Nombre"] == nombreEstacion)]

        # generar indice como fecha
        dataGrafica.index = dataGrafica["Fecha"]
        dataGrafica.index = pd.to_datetime(dataGrafica.index)

        ##### Generar gráfica
        # iniciar la gráfica
        plt.clf()

        # configurar tamaño de gráfica
        fig = plt.figure(figsize=(15,5))
        ax = fig.add_subplot(111)

        # obtener x, y , e
        x = np.array(dataGrafica.index.hour)
        y = np.array(dataGrafica["RainWRF"])
        e = np.array(dataGrafica["validacionEvento"])

        # configurar línea
        line, = ax.plot(x, y, lw=2, color='r')

        # generar títulos
        tituloGrafica = "CAÑON ANTIGRANIZO: {}\n{}-{}-{}".format(nombreEstacion, anio, mes, dia)

        # configurar títulos
        #ax.set_xlabel("HORA")
        ax.set_ylabel("PP (mm)")
        #ax.set_title(tituloGrafica)

        # crear anotación
        ax.annotate('EVENTO', xy=(x[e.argmax()]+1, y.max()/2), xytext=(x[e.argmax()]+2, y.max()/2), arrowprops=dict(facecolor='red', shrink=0.02))

        # guardar gráfica
        nombreTemporalGrafica = "data/graphs/eventos/{}_{}-{}-{}_wrf.png".format(nombreEstacion, anio, mes, dia)
        plt.savefig(nombreTemporalGrafica, dpi=600, bbox_inches='tight')

        # print
        print("Graph: {} Fecha: {}-{}-{}".format(nombreEstacion, anio, mes, dia))

    # # zip imagenes
    # comando = "zip -r data/prueba{}.zip data/graphs".format(prueba)
    # os.system(comando)


# declarar función main
if __name__ == '__main__':
    main()
