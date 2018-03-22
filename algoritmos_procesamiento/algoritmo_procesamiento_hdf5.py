#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 16:17:25 2017

@author: jorgemauricio
"""

# librerias
import h5py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from numpy import meshgrid
from scipy.interpolate import griddata as gd
import os

# programa principal
def main():

	# obtener coordenadas cañones antigranizo
	dataAntigranizo = pd.read_csv("data/Coordenadas_caniones.csv")

	# Nombre del archivo
	# filename = 'data/3B-HHR-L.MS.MRG.3IMERG.20180101-S000000-E002959.0000.V05B.HDF5'

	# obtener archivos
	listaDeArchivos = [x for x in os.listdir('data/hdf5') if x.endswith('HDF5')]
	# print(listaDeArchivos)
	# ciclo de procesamiento de datos
	for nombre in listaDeArchivos:
		# ruta temporal de archivo
		nombreTemporalArchivo = "data/hdf5/{}".format(nombre)

		#lectura del hdf5
		f = h5py.File(nombreTemporalArchivo, 'r')

		# variable temporal para procesar el hdf5
		grid = f['Grid']

		# arrays de numpy
		lon = np.array(grid['lon'])
		lat = np.array(grid['lat'])
		precipitation = np.array(grid['precipitationCal'])

		# crear la variable que guardara el texto
		dataText = "Long,Lat,Prec\n"
		for i in range(lon.shape[0]):
		    for j in range(lat.shape[0]):
		        tempText = "{},{},{}\n".format(lon[i], lat[j], precipitation[i,j])
		        dataText += tempText


		# generar variables extras
		nombreEnArray = nombre.split('.')

		# fecha y minutos
		tempfecha = nombreEnArray[4]
		minutos = nombreEnArray[5]

		fecha, temp1, temp2 = tempfecha.split('-')

		# guardar a CSV
		nombreArchivoParaPandas = guardarCSV(dataText, fecha, minutos)

		# leer archivo en pandas
		data = pd.read_csv(nombreArchivoParaPandas)

		# limites longitud > -106.49 y < -97.5
		data = data.loc[data['Long'] > -106.49]
		data = data.loc[data['Long'] < -97.5]

		# limites latitud > 17.43 y < 25.23
		data = data.loc[data['Lat'] > 17.43]
		data = data.loc[data['Lat'] < 25.23]

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
		    stepVariable = 5

		clevs = np.linspace(z.min(), z.max() + 5, 10)
		#clevs = [0,5,10,15,20,25,30,45,60,75]
		clevs = [1,5,10,30,50,70,100,150,300,500]

		#%% contour plot
		cs = m.contourf(xi,yi,zi, clevs, zorder=5, alpha=0.5, cmap='rainbow')

		# draw map details
		#m.drawcoastlines()

		#m.drawstates(linewidth=0.7)
		#m.drawcountries()

		#%% read municipios shape file
		#m.readshapefile('shapes/MunicipiosAgs', 'Municipios')
		m.readshapefile('shapes/Estados', 'Estados')

		m.scatter(xC, yC, latlon=True,s=1, marker='o', color='r', zorder=25)

		#%% colorbar
		cbar = m.colorbar(cs, location='right', pad="5%")
		cbar.set_label('mm')
		tituloTemporalParaElMapa = "Precipitación {} {}".format(fecha, minutos)
		plt.title(tituloTemporalParaElMapa)
		# Mac /Users/jorgemauricio/Documents/Research/proyectoGranizo/data/Maps/{}_{}.png
		# Linux /home/jorge/Documents/Research/proyectoGranizo/data/Maps/{}_{}.png
		nombreTemporalParaElMapa = "/home/jorge/Documents/Research/proyectoGranizo/data/Maps/{}_{}.png".format(fecha,minutos)
		plt.annotate('@2018 INIFAP', xy=(-102,22), xycoords='figure fraction', xytext=(0.45,0.45), color='g', zorder=50)

		plt.savefig(nombreTemporalParaElMapa, dpi=300)
		print('****** Genereate: {}'.format(nombreTemporalParaElMapa))

		# nombre para eliminar el archivo temporal
		nombreTemporalArchivoEliminar = 'temp/{}_{}.csv'.format(fecha, minutos)
		os.remove(nombreTemporalArchivoEliminar)
		print("Eliminar: {}".format(nombreTemporalArchivoEliminar))
		# cerrar archivo hdf5
		f.close()


def generarNombreDelMapa(nombre):
	"""
	Función que genera el título del mapa
	param: nombre: nombre del archivo
	"""

def guardarCSV(variableTexto, fecha, minutos):
	"""
	Función que permite guardar una viriable de texto  a .csv
	param: txt: variable de texto a guardar
	"""
	fileName = 'temp/{}_{}.csv'.format(fecha, minutos)
	textFile = open(fileName, "w")
	textFile.write(variableTexto)
	textFile.close()
	return fileName


if __name__ == '__main__':
    main()
