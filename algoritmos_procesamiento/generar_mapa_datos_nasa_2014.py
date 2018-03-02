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
import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from scipy.interpolate import griddata as gd
from time import gmtime, strftime

# Programa principal
def main():
	# limpiar la terminal
	os.system('clear')

	# Estructura final de base de datos
	dataBaseStructureCaniones =  "Canon,Estado,Nombre,Long,Lat,Year,Month,Day,Hour,RainIMR\n"

	# ruta para guardar nombreArchivoParaPandas

	# Obtener todos los archivos en data
	#listaDeFechas = ['2018-01-01']
	# listaDeFechas = [x for x in os.listdir('/media/jorge/U/WRF_Granizo') if x.endswith('')]

	# obtener coordenadas cañones dataAntigranizo
	dataAntigranizo = pd.read_csv("data/Coordenadas_caniones.csv")

	#%% generar info
	#%% -106.49 > Long > -97.5
	#%% 17.43 > Lat > 25.23

	# ruta temporal folders
	rutaTemporalDeArchivos = "/media/jorge/backup1/gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.04"
	# generar lista de archvos para procesamiento
	#listaDeArchivos = [x for x in os.listdir(rutaTemporalDeArchivos) if x.endswith('')]
	listaDeArchivos = ['2014']
	# ciclo de procesamiento
	for folderAnio in listaDeArchivos:

		# ruta temporal de archivo
		nombreTemporalDelFolderAnio = "/media/jorge/backup1/gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.04/{}".format(folderAnio)

		# lista de archivos diarios
		listaDeArchivosDeDias = [x for x in os.listdir(nombreTemporalDelFolderAnio) if x.endswith('')]

		for folderDia in listaDeArchivosDeDias:

			# ruta temporal de archivo de dias
			nombreTemporalDelFolderDia = "/media/jorge/backup1/gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.04/{}/{}".format(folderAnio,folderDia)

			# lista de archivos en folder diarios
			listaDeArchivosEnFolderDia = [x for x in os.listdir(nombreTemporalDelFolderDia) if x.endswith('.HDF5')]

			# for
			for nombreDelArchivo in listaDeArchivosEnFolderDia:

				# nombre temporal del archivo a procesar
				nombreTemporalArchivo = "/media/jorge/backup1/gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.04/{}/{}/{}".format(folderAnio,folderDia, nombreDelArchivo)

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
				nombreEnArray = nombreDelArchivo.split('.')

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

				#clevs
				clevs = [1,5,10,20,30,50,70,100,150,300,500]
				#clevs = [0,5,10,15,20,25,30,45,60,75]

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
				cbar = m.colorbar(cs, location='bottom', pad="5%")
				cbar.set_label('mm')
				tituloTemporalParaElMapa = "Precipitación para la hora: {}".format(nombreTemporalHora)
				plt.title(tituloTemporalParaElMapa)
				# Mac /Users/jorgemauricio/Documents/Research/proyectoGranizo/Maps/{}_{}.png
				# Linux /home/jorge/Documents/Research/proyectoGranizo/Maps/{}_{}.png
				nombreTemporalParaElMapa = "/home/jorge/Documents/Research/proyectoGranizo/data/mapsNASA/{}_{}.png".format(tempfecha,minutos)
				plt.annotate('@2018 INIFAP', xy=(-102,22), xycoords='figure fraction', xytext=(0.45,0.45), color='g', zorder=50)

				plt.savefig(nombreTemporalParaElMapa, dpi=300)
				print('****** Genereate: {}'.format(nombreTemporalParaElMapa))

				print(nombreArchivoParaPandas)
				eliminarCSVTemporal(nombreArchivoParaPandas)

	#%% Guardar a CSV
	fileName = 'data/dataFromCanionesTestNASA_2014.csv'
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

def eliminarCSVTemporal(nombreDelArchivo):
	os.remove(nombreDelArchivo)

if __name__ == '__main__':
	main()
