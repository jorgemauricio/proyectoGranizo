#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite inteporlar datos
# de precipitación de la NASA
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
import h5py

# Programa principal
def main():
	# limpiar la terminal
	os.system('clear')

	# Estructura final de base de datos
	dataBaseStructureCaniones =  "Canon,Estado,Nombre,Long,Lat,Year,Month,Day,Hour,RainIMR\n"

	# Obtener todos los archivos en data
	#listaDeFechas = ['2018-01-01']
	# listaDeFechas = [x for x in os.listdir('/media/jorge/U/WRF_Granizo') if x.endswith('')]

	# obtener coordenadas cañones dataAntigranizo
	dataAntigranizo = pd.read_csv("data/Coordenadas_caniones.csv")

	#%% generar info
	#%% -106.49 > Long > -97.5
	#%% 17.43 > Lat > 25.23

	# ruta temporal archivo
	rutaTemporalDeArchivos = "data/hdf5"
	# generar lista de archvos para procesamiento
	listaDeArchivos = [x for x in os.listdir(rutaTemporalDeArchivos) if x.endswith('.HDF5')]

	# ciclo de procesamiento
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

		# close hdf5
		f.close()

		# leer archivo en pandas
		data = pd.read_csv(nombreArchivoParaPandas)

		# determinar la hora de lectura
		nombreTemporalHora = minutos
		#print("***** nombre temporal hora", nombreTemporalHora)

		# limites longitud > -106.49 y < -97.5
		data = data.loc[data['Long'] > -106.49]
		data = data.loc[data['Long'] < -97.5]

		# limites latitud > 17.43 y < 25.23
		data = data.loc[data['Lat'] > 17.43]
		data = data.loc[data['Lat'] < 25.23]

		# ciclo para generar información
		for index, row in dataAntigranizo.iterrows():
			# determinar fecha
			#year, month, day = fecha.split('-')
			year = fecha[0:4]
			month = fecha[4:6]
			day = fecha[6:8]

			#print("***** {},{},{}".format(year, month, day))
			# generar np arrays
			Lat = np.array(data['Lat'])
			Long = np.array(data['Long'])
			Rain = np.array(data['Prec'])

			# Punto a evaluar
			pointLat = float(row['Lat'])
			pointLong = float(row['Long'])
			pointEstado = row['Estado']
			pointNumber = row['ID']
			pointNombre = row['Nombre']

			# distancias
			d1 = 0.0
			d2 = 0.0
			d3 = 0.0
			pointIndex1 = 0.0
			pointIndex2 = 0.0
			pointIndex3 = 0.0

			# Selección de los puntos para interpolación
			for i in range(len(Lat)):
				distanceBetweenPoints = 0.0
				differenceX = pointLong - Long[i]
				differenceY = pointLat - Lat[i]
				sumDifferenceXY = pow(differenceX, 2.0) + pow(differenceY, 2.0)
				distanceBetweenPoints = math.sqrt(sumDifferenceXY)
				if i == 0:
					d1 = distanceBetweenPoints
					pointIndex1 = i
					d2 = distanceBetweenPoints
					pointIndex2 = i
					d3 = distanceBetweenPoints
					pointIndex3 = i
				if distanceBetweenPoints < d1:
					d3 = d2
					pointIndex3 = pointIndex2
					d2 = d1
					pointIndex2 = pointIndex1
					d1 = distanceBetweenPoints
					pointIndex1 = i
				if distanceBetweenPoints > d1 and distanceBetweenPoints < d2:
					d3 = d2
					pointIndex3 = pointIndex2
					d2 = distanceBetweenPoints
					pointIndex2 = i
				if distanceBetweenPoints > d2 and distanceBetweenPoints < d3:
					d3 = distanceBetweenPoints
					pointIndex3 = i

			# intepolación
			k = 2.0
			w1 = 0.0
			w2 = 0.0
			w3 = 0.0
			zGraupel = 0.0

			inverseSum = pow((1 / d1),k) + pow((1 / d2),k) + pow((1 / d3),k)
			w1 = 1 / pow(d1,k) / inverseSum
			w2 = 1 / pow(d2,k) / inverseSum
			w3 = 1 / pow(d3,k) / inverseSum

			zRain = (w1 * Rain[pointIndex1]) + (w2 * Rain[pointIndex2]) + (w3 * Rain[pointIndex3])

			# Estructura
			dataBaseStructureCaniones += '{},{},{},{},{},{},{},{},{},{}\n'.format(pointNumber, pointEstado, pointNombre, pointLong, pointLat, year, month, day, nombreTemporalHora, zRain)

	#%% Guardar a CSV
	fileName = 'data/dataFromCanionesTestImer.csv'
	textFile = open(fileName, "w")
	textFile.write(dataBaseStructureCaniones)
	textFile.close()

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
