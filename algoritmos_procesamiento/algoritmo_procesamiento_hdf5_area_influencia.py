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

	# distancia
	DISTANCIA_1KM = 0.0043
	# obtener coordenadas cañones antigranizo
	dataAntigranizo = pd.read_csv("data/Coordenadas_caniones.csv")
	#print(dataAntigranizo.head())

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

		# ciclo de área de influencia
		# iniciar con el procesamiento
		for i in range(0, dataAntigranizo["Nombre"].count()):
			# generar variables para la clasificación de información
			# Nombre
			nombreEstacion = dataAntigranizo.iloc[i]["Nombre"]
			# Latitud
			latitud = dataAntigranizo.iloc[i]["Lat"]
			# Mes
			longitud = dataAntigranizo.iloc[i]["Long"]

			longitud_min = longitud - (3 * DISTANCIA_1KM)
			longitud_max = longitud + (3 * DISTANCIA_1KM)

			latitud_min = latitud - (3 * DISTANCIA_1KM)
			latitud_max = latitud + (3 * DISTANCIA_1KM)

			# limites longitud > -106.49 y < -97.5
			data = data.loc[data['Long'] > -106.49]
			data = data.loc[data['Long'] < -97.5]

			# limites latitud > 17.43 y < 25.23
			data = data.loc[data['Lat'] > 17.43]
			data = data.loc[data['Lat'] < 25.23]

			x = np.array(data['Long'])
			y = np.array(data['Lat'])

			# numero de columnas y filas
			numCols = len(x)
			numRows = len(y)

			# generar xi, yi
			xi = np.linspace(longitud_min, longitud_max, numCols)
			yi = np.linspace(longitud_min, latitud_max, numRows)

			# generar el meshgrid
			xi, yi = np.meshgrid(xi, yi)

			# generar zi
			z = np.array(data['Prec'])
			zi = gd((x,y), z, (xi,yi), method='cubic')



			fileName = 'temp/test_zi.csv'
			np.savetxt(fileName, zi, delimiter=",")

			break
			# print data
			print("***** ",nombreEstacion)

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
