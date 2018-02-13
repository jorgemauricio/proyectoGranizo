#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:17:25 2017

@author: jorgemauricio
"""

# librerias
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata as gd
from time import gmtime, strftime
import time
import os

def main():
    # generar lista de fechas disponibles
    # Mac /Volumes/U/WRF_Granizo path donde se encuentran los archivos
    # Linux /media/U/WRF_Granizo
    # Mac listaDeFechas = [x for x in os.listdir('/Volumes/U/WRF_Granizo') if x.endswith('')]
    # Linux listaDeFechas = [x for x in os.listdir('/media/U/WRF_Granizo') if x.endswith('')]
    listaDeFechas = ['2018-01-01']
    # obtener coordenadas cañones antigranizo
    dataAntigranizo = pd.read_csv("../data/Coordenadas_caniones.csv")

    # ciclo de procesamiento de información
    for i in listaDeFechas:
        # nombre temporal de la ruta
        rutaTemporalDeArchivos = "/media/jorge/U/WRF_Granizo/{}".format(i)
        print(rutaTemporalDeArchivos)
        # generar lista de archvos para procesamiento
        listaDeArchivos = [x for x in os.listdir(rutaTemporalDeArchivos) if x.endswith('')]

        # ciclo de procesamiento
        for j in listaDeArchivos:
            # nombre temporal del archivo a procesar
            nombreTemporalDeArchivo = "{}/{}".format(rutaTemporalDeArchivos, j)

            # leer datos de archivos
            data = pd.read_csv(nombreTemporalDeArchivo)

            # determinar la hora de lectura
            arrayTemporalHora = j.split('_')
            nombreTemporalHora = int(arrayTemporalHora[1])

            # limites longitud > -106.49 y < -97.5
            data = data.loc[data['Long'] > -106.49]
            data = data.loc[data['Long'] < -97.5]

            # limites latitud > 17.43 y < 25.23
            data = data.loc[data['Lat'] > 17.43]
            data = data.loc[data['Lat'] < 25.23]

            # generar precipitación
            data['Prec'] = data.apply(lambda x: convertDBZtoPrec(x['Ref (dbz)']), axis=1)

            # generar granizo
            data['Granizo'] = data.apply(lambda x: convertDBZtoGranizo(x['Ref (dbz)']), axis=1)

            # obtener valores de x, y
            lons = np.array(data['Long'])
            lats = np.array(data['Lat'])

            #%% iniciar la gráfica
            plt.clf()

            # agregar locación de Coordenadas_caniones
            xC = np.array(dataAntigranizo['Long'])
            yC = np.array(dataAntigranizo['Lat'])
            #plt.scatter(xC, yC,3, marker='o', color='r', zorder=25)
            # fig = plt.figure(figsize=(48,24))
            m = Basemap(projection='mill',llcrnrlat=17.43,urcrnrlat=25.23,llcrnrlon=-106.49,urcrnrlon=-97.5,resolution='h')

            # generar lats, lons
            x, y = m(lons, lats)

            # numero de columnas y filas
            numCols = len(x)
            numRows = len(y)

            # generar xi, yi
            xi = np.linspace(x.min(), x.max(), numCols)
            yi = np.linspace(y.min(), y.max(), numRows)

            # generar el meshgrid
            xi, yi = np.meshgrid(xi, yi)

            # generar zi
            z = np.array(data['Prec'])
            zi = gd((x,y), z, (xi,yi), method='cubic')

            # generar clevs
            stepVariable = 1
            step = (z.max() - z.min()) / 10

            # verificar el valor del intervalo
            if step <= 1:
                stepVariable = 3

            clevs = np.linspace(z.min(), z.max() + ( step * stepVariable ), 10)
            #clevs = [0,5,10,15,20,25,30,45,60,75]

            #%% contour plot
            cs = m.contourf(xi,yi,zi, clevs, zorder=5, alpha=0.5, cmap='PuBu')

            # draw map details
            #m.drawcoastlines()

            #m.drawstates(linewidth=0.7)
            #m.drawcountries()

            #%% read municipios shape file
            #m.readshapefile('shapes/MunicipiosAgs', 'Municipios')
            m.readshapefile('../shapes/Estados', 'Estados')

            m.scatter(xC, yC, latlon=True,s=1, marker='o', color='r', zorder=25)

            #%% colorbar
            cbar = m.colorbar(cs, location='right', pad="5%")
            cbar.set_label('mm')
            tituloTemporalParaElMapa = "Precipitación para la hora: {}".format(nombreTemporalHora)
            plt.title(tituloTemporalParaElMapa)
            # Mac /Users/jorgemauricio/Documents/Research/proyectoGranizo/Maps/{}_{}.png
            # Linux /home/jorge/Documents/Research/proyectoGranizo/Maps/{}_{}.png
            nombreTemporalParaElMapa = "/home/jorge/Documents/Research/proyectoGranizo/Maps/{}_{}.png".format(i,j)
            plt.annotate('@2018 INIFAP', xy=(-102,22), xycoords='figure fraction', xytext=(0.45,0.45), color='g', zorder=50)

            plt.savefig(nombreTemporalParaElMapa, dpi=300)
            print('****** Genereate: {}'.format(nombreTemporalParaElMapa))


def convertDBZtoPrec(dbz):
    """
    Funcion para convertir el valor de dbz a lluvia
    param: dbz :  valor
    """
    rain = ((10**(dbz/10))/200)**(5/8)
    if rain <= 1:
        return 0
    else:
        return rain

def convertDBZtoGranizo(dbz):
    """
    Funcion para convertir el valor de dbz a granizo
    param: dbz :  valor
    """
    if dbz >= 55:
        granizo = ((10**(dbz/10))/200)**(5/8)
        if granizo <= 1:
            return 0
        else:
            return granizo
    else:
        return 0

if __name__ == '__main__':
    main()
