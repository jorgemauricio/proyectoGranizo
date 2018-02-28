#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite la interpolación de los
# datos de precipitación de la NASA
# Author: Jorge Mauricio
# Email: jorge.ernesto.mauricio@gmail.com
# Date: 2018-02-01
# Version: 1.0
#######################################
"""
#!/usr/bin/env python3 # -*- coding: utf-8 -*-
"""
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
    nombreTemporalArchivo = "{}/data/dataFromNASA_Compilado.csv".format(path)

    # leer csv
    data = pd.read_csv(nombreTemporalArchivo)

    # iniciar con el procesamiento
    for nombre in data["Nombre"].unique():
        # clasificar la información por nombre
        dataTemp = data.loc[data["Nombre"] == nombre]

        # organizar la información por listaDeFechas
        dataTemp = dataTemp.sort_values(by=["Year","Month","Day","Hour"])

        # crear columna de diferencia
        dataTemp["diff"] = dataTemp["RainIMR"] - dataTemp["RainIMR"].shift(1)

        # generar rango de diff
        dataTemp["Rango"] = dataTemp.apply(lambda x: generarRango(x["diff"]), axis=1)

        # eliminar datos nulos
        dataTemp = dataTemp.dropna()

        # evitar columnas ajenas
        dataTemp = dataTemp[["Canon", "Estado", "Nombre", "Long", "Lat", "Year", "Month", "Day", "Hour", "RainIMR", "diff", "Rango"]]

        # agregar df temporal a frames
        frames.append(dataTemp)

        # procesamiento de {}
        print("procesamiento de:", nombre)

    # generar un solo archivo
    data = pd.concat(frames)

    # generar variables descriptivas
    for rango in data["Rango"].unique():
        data[rango] = [1 if x == rango else 0 for x in data["Rango"]]

    # guardar archivo a CSV
    nombreArchivoFinal = "{}/data/Resultado.csv".format(path)
    data.to_csv(nombreArchivoFinal, index=False)

def generarRango(valor):
    if valor >= 0 and valor <= 5:
        return "0-5"
    if valor > 5 and valor <= 10:
        return "5-10"
    if valor > 10 and valor <= 15:
        return "10-15"
    if valor > 15 and valor <= 20:
        return "15-20"
    if valor > 20 and valor <= 25:
        return "20-25"
    if valor > 25 and valor <= 30:
        return "25-30"
    if valor > 30:
        return ">30"

if __name__ == '__main__':
    main()
