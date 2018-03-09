#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite convertir la hora decimal
# a segundos
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
    nombreTemporalArchivo = "{}/data/datos_inteporlados_30min_wrf.csv".format(path)

    # leer csv
    data = pd.read_csv(nombreTemporalArchivo)

    data["Hora_Formato"] = data.apply(lambda x: convertir_hora_decimal_a_hora_minutal(x["Hour"]), axis=1)

    # guardar csv
    data.to_csv("data/datos_interpolados_30_min_con_formato_wrf-csv")

def convertir_hora_decimal_a_hora_minutal(h):
    h = str(h)
    hora, minutos = h.split(".")
    if len(hora) < 2:
        hora = "0{}".format(hora)

    if minutos == "5":
        minutos = "30"
    else:
        minutos = "00"
    tiempo = "{}:{}".format(hora, minutos)

    return tiempo

# declarar función main
if __name__ == '__main__':
    main()
