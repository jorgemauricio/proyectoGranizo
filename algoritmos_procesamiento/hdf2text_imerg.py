#Code produced through UMBC's Joint Center for Earth Systems Technology
#If you have any questions or concerns regarding the following script, please contact Amanda Rumsey at arumsey@umbc.edu
#The purpose of this code is to convert datasets within imerg hdf files to txt files

#start of the program
print("starting the conversion from hdf to txt file:")
print("")

#import all necessary packages
print("importing packages")
import os
import glob
import numpy as np
import h5py
print("packages imported")
print("")

#list of methods 
#this method will print all of the names of the hdf internal files
print("defining methods")
def printname(name):
	print(name)
print("method definitions complete")
print("")
	
#assign current working directory
dir=os.getcwd()
print("the current directory is: "+dir)
print("")

#make directory folder (if it does not already exist) and directory variable for output text files
print("creating a directory for output text files")
if not os.path.exists(dir+"/"+"text_files/"):
	os.makedirs(dir+"/"+"text_files/")
txtdir=dir+"/"+"text_files"
print("text file directory created")
print("")

#list of hdf files to be converted
print("list of hdf files")
hdflist=glob.glob(os.path.join('*.HDF5'))
print(hdflist)
print("")

#available datasets in hdf files
print("available datasets in HDF5 files: ")
singlehdflist=hdflist[0]
insidehdffile=h5py.File(singlehdflist,"r+")
insidehdffile.visit(printname)
insidehdffile.close()
print("")

#datatype conversion 
#this loop outputs the indvidual lat long and precip datasets available within the hdf file as indivdual text files
for hdffile in hdflist:
	#read and write hdf file
	print("reading the hdf file: "+hdffile)
	currenthdffile=h5py.File(hdffile,"r+")
	print("reading hdf file complete")
	print("")
	
	#data retrieval 
	#This is where you extract the datasets you want to output as text files
	#you can add more variables if you would like
	#this is done in the format varible=hdffilename['dataset']
	print("creating arrays for latitude, longitude and surface precipitation")
	lat=currenthdffile['Grid/lat']
	long=currenthdffile['Grid/lon']
	precip=currenthdffile['Grid/precipitation']
	latitude=np.array(lat)
	longitude=np.array(long)
	precipitation=np.array(precip)
	print("creation of arrays complete")
	print("")
	
	#converting to text file
	print("converting arrays to text files")
	outputlat=txtdir+"/"+hdffile[:-5]+"_lat.txt"
	outputlong=txtdir+"/"+hdffile[:-5]+"_long.txt"
	outputprecip=txtdir+"/"+hdffile[:-5]+"_precip.txt"
	np.savetxt(outputlat,latitude,fmt='%f')
	np.savetxt(outputlong,longitude,fmt='%f')
	np.savetxt(outputprecip,precipitation,fmt='%f')
	print("")

print("script complete!")
	
	
