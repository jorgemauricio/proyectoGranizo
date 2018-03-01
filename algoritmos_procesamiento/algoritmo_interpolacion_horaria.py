#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#######################################
# Script que permite crear gráficas a partir
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

	# Estructura final de base de datos
	dataBaseStructureCaniones =  "Canon,Estado,Nombre,Long,Lat,Year,Month,Day,Hour,GraupelWRF,RainWRF,TproWRF\n"

	# Obtener todos los archivos en data
	# listaDeFechas = ['2017-09-01']
	listaDeFechas = [x for x in os.listdir('/media/jorge/U/WRF_Granizo') if x.endswith('')]

	# obtener coordenadas cañones dataAntigranizo
	dataAntigranizo = pd.read_csv("../data/Coordenadas_caniones.csv")

	#%% generar info
	#%% -106.49 > Long > -97.5
	#%% 17.43 > Lat > 25.23

	for z in listaDeFechas:
		# nombre temporal de la ruta
		rutaTemporalDeArchivos = "/media/jorge/U/WRF_Granizo/{}".format(z)
		fecha = z

		# generar lista de archvos para procesamiento
		listaDeArchivos = [x for x in os.listdir(rutaTemporalDeArchivos) if x.endswith('')]

		# ciclo de procesamiento
		for j in range(7,32,1):
			if len(str(j)) == 1:
				titulo = "00{}".format(j)
			else:
				titulo = "0{}".format(j)

			# nombre temporal del archivo a procesar
			nombreTemporalDeArchivo = "{}/Vars_{}".format(rutaTemporalDeArchivos, titulo)
			#print("***** nombre temporal de archivo", nombreTemporalDeArchivo)

			# leer datos WRF de archivos
			data = pd.read_csv(nombreTemporalDeArchivo)

			# determinar la hora de lectura
			nombreTemporalHora = j
			#print("***** nombre temporal hora", nombreTemporalHora)

			# limites longitud > -106.49 y < -97.5
			data = data.loc[data['Long'] > -106.49]
			data = data.loc[data['Long'] < -97.5]

			# limites latitud > 17.43 y < 25.23
			data = data.loc[data['Lat'] > 17.43]
			data = data.loc[data['Lat'] < 25.23]

			# generar precipitación
			data['Rain'] = data.apply(lambda x: convertDBZtoPrec(x['Ref (dbz)']), axis=1)

			# generar granizo
			data['Granizo'] = data.apply(lambda x: convertDBZtoGranizo(x['Ref (dbz)']), axis=1)

			# ciclo para generar información
			for index, row in dataAntigranizo.iterrows():
				# determinar fecha
				year, month, day = fecha.split('-')
				#print("***** {},{},{}".format(year, month, day))
				# generar np arrays
				Lat = np.array(data['Lat'])
				Long = np.array(data['Long'])
				Rain = np.array(data['Rain'])
				Graupel = np.array(data['Granizo'])
				Tpro = np.array(data['Temp (°C)'])

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
				zTpro = 0.0
				zRain = 0.0
				zGraupel = 0.0

				inverseSum = pow((1 / d1),k) + pow((1 / d2),k) + pow((1 / d3),k)
				w1 = 1 / pow(d1,k) / inverseSum
				w2 = 1 / pow(d2,k) / inverseSum
				w3 = 1 / pow(d3,k) / inverseSum

				zTpro = (w1 * Tpro[pointIndex1]) + (w2 * Tpro[pointIndex2]) + (w3 * Tpro[pointIndex3])
				zRain = (w1 * Rain[pointIndex1]) + (w2 * Rain[pointIndex2]) + (w3 * Rain[pointIndex3])
				zGraupel = (w1 * Graupel[pointIndex1]) + (w2 * Graupel[pointIndex2]) + (w3 * Graupel[pointIndex3])

				# Estructura
				dataBaseStructureCaniones += '{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(pointNumber, pointEstado, pointNombre, pointLong, pointLat, year, month, day, nombreTemporalHora, zGraupel, zRain, zTpro)

	#%% Guardar a CSV
	fileName = '../data/dataFromCanionesTest.csv'
	textFile = open(fileName, "w")
	textFile.write(dataBaseStructureCaniones)
	textFile.close()

def convertDBZtoPrec(dbz):
    """
    Funcion para convertir el valor de dbz a lluvia
    param: dbz :  valor
    """
    rain = ((10**(dbz/10))/200)**(5/8)
    if rain <= 1:
        return 0.0
    elif rain == np.inf:
    	return 0.0
    elif rain == np.nan:
        return 0.0
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
            return 0.0
        elif granizo == np.inf:
        	return 0.0
        elif granizo == np.nan:
        	return 0.0
        else:
            return granizo
    else:
        return 0

if __name__ == '__main__':
    main()
