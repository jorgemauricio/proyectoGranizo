#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:17:25 2017

@author: jorgemauricio
"""

import os
import pandas as pd
import numpy as np

#%% fecha del pronostico
fechaPronostico = '2013-11-05'

#%% generate arrayFechas
# Generate Days
fechasSinDatos = []
arrayFechas = []
tanio, tmes, tdia = fechaPronostico.split('-')
anio = int(tanio)
mes = int(tmes)
dia = int(tdia)

for i in range(0,1450,1):
    if i == 0:
        newDiaString = '{}'.format(dia)
        if len(newDiaString) == 1:
            newDiaString = '0' + newDiaString
        newMesString = '{}'.format(mes)
        if len(newMesString) == 1:
            newMesString = '0' + newMesString
        fecha = '{}'.format(anio)+"-"+newMesString+"-"+newDiaString
    if i > 0:
        dia = dia + 1
        if mes == 2 and anio % 4 == 0:
            diaEnElMes = 29
        elif mes == 2 and anio % 4 != 0:
            diaEnElMes = 28
        elif mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12:
            diaEnElMes = 31
        elif mes == 4 or mes == 6 or mes == 9 or mes == 11:
            diaEnElMes = 30
        if dia > diaEnElMes:
            mes = mes + 1
            dia = 1
        if mes > 12:
            anio = anio + 1
            mes = 1
        newDiaString = '{}'.format(dia)
        if len(newDiaString) == 1:
            newDiaString = '0' + newDiaString
        newMesString = '{}'.format(mes)
        if len(newMesString) == 1:
            newMesString = '0' + newMesString
        fecha = '{}'.format(anio)+"-"+newMesString+"-"+newDiaString
        # /Volumes/U/WRF_Granizo/ dirección en mi Laptop
        tempPath = "/media/jorge/U/WRF_Granizo/{}".format(fecha)
        if os.path.exists(tempPath):
            print("Fecha: {} *** Ok".format(fecha))
            tempPath2 = "/media/jorge/U/WRF_Granizo/{}/Vars_007".format(fecha)
            if os.path.isfile(tempPath2):
                print("***** Fecha {} : Ok".format(fecha))
                # for j in range(32,128,1):
                #     if j < 100:
                #         tempFileName = "Vars_0{}".format(j)
                #     else:
                #         tempFileName = "Vars_{}".format(j)
                #     tempPath3 = "/Volumes/U/WRF_Granizo/{}/{}".format(fecha, tempFileName)
                #     print("Eliminar: {}".format(tempFileName))
                #     os.remove(tempPath3)
            else:
                fechasSinDatos.append(fecha)
                print("***** Fecha {} : Error".format(fecha))
                print("Guardar para verificar")
        else:
            print("Fecha: {} *** Error".format(fecha))
            arrayFechas.append(fecha)

print("Días sin pronostico: {}".format("\n".join(arrayFechas)))
print("Sin datos: {}".format("\n".join(fechasSinDatos)))
