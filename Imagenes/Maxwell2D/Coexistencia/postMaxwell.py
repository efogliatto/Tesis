import os

import numpy as np

import matplotlib.pyplot as plt

import argparse

import glob

from paraview.simple import *






if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución del problema de construcción de Maxwell para diferentes constantes')

    args = parser.parse_args()


    # Lista con parametros

    paramList = [ [0.5, 4.0, 1.25] ]


    # Directorio del caso y limpieza
    
    main_dir = os.getcwd()
    


    # Movimiento en todos los parametros
    
    for param in paramList:


        # Deteccion de Temperaturas simuladas
        
        cases_dir = 'a_{:.4f}_b_{:.4f}_sigma_{:.4f}/'.format( param[0], param[1], param[2] )

        flist = glob.glob( cases_dir + '/Tr_' + '*' )    
       
        trlist = {}

        for a in flist:
         
            trlist[a] = float( a[len(cases_dir)+3:] )



        # Carga del caso en paraview

        rhogList = []

        rholList = []

        TList = []

        for fname, Tr in trlist.items():


            TList.append(Tr)
            

            lbmcase = EnSightReader( CaseFileName = fname + '/lbm.case')

            times = lbmcase.TimestepValues

            lbmcase.PointArrays = ['rho']


            # Ultimo paso de tiempo


            # Valores maximos



        



        


    


    
