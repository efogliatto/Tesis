import vdWColumn as vdw

import vdWColumn.postLBRun as post

import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

import glob

from paraview.simple import *

from scipy import stats

import locale





# Extraccion de arreglos en linea desde el centro (xmax/2) hasta xmax

def get_array_from_case( case_file, array_name = 'rho', xmax = 300.0 ):


    # Carga del caso con arrays para rho y p
    
    lbmcase = EnSightReader(CaseFileName=case_file)

    times = lbmcase.TimestepValues

    lbmcase.PointArrays = [array_name]


    
    # Filtro Plot over line

    POL = PlotOverLine(Input=lbmcase, Source='High Resolution Line Source')

    POL.Tolerance = 2.0e-16

    POL.Source.Point1 = [0.0, xmax/2.0, xmax/2.0]

    POL.Source.Point2 = [xmax, xmax/2.0, xmax/2.0]

    POL.Source.Resolution = (int)(xmax)


    
    # Alocacion de arreglos

    Array = np.array( range(POL.Source.Resolution+1), dtype=np.float64() )



    # Extraccion del ultimo paso de tiempo

    POL.UpdatePipeline( time = times[-1] )    

    POLf = servermanager.Fetch(POL)
   
    for id in range( POL.Source.Resolution+1 ):
        
        Array[id] = POLf.GetPointData().GetArray(array_name).GetValue(id)

  
    

    return Array






def get_deltaP( kappaList ):


    kdict = {}
    
    

    for i,kappa in enumerate(kappaList):


        # Data lists

        deltaP = []

        rlist = []
            
            

        # Folder name
            
        flist = glob.glob( 'kappa_{}/'.format(kappa) + 'Caso*' )

        for f in flist:


            # Diferencia de presion

            lbp = get_array_from_case( case_file = f + '/lbm.case', array_name = 'p', xmax = 200.0 )

            deltaP.append( lbp[ int(len(lbp)/2) ] - lbp[0] )



            # Radio efectivo

            lbRho = get_array_from_case( case_file = f + '/lbm.case', array_name = 'rho', xmax = 200.0 )

            ycross, bl, tl = post.interphase( lbRho[ int(len(lbRho)/2): ], fw=True, width=0.05 )

            rlist.append(1/ycross)



        # Incorporacion al diccionario

        kdict[kappa] = ( rlist, deltaP )



    # Escritura del diccionario

    with open( 'deltaP.dat', 'w' ) as f:

        for k in kappaList:

            rad = kdict[k][0]

            dp = kdict[k][1]


            for r,d in zip(rad,dp):

                f.write('{} {} {}\n'.format(k,r,d))

            

    







if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resoluci\'on de Ley de Laplace')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')

    parser.add_argument('-onlyPlot', help='Solo genera la imagen', action='store_true')

    args = parser.parse_args()

      

    # Perfiles de densidad

    colorList = ['r', 'b', 'g', 'y', 'orange']

    mkList = ['o', 's', '^', '*', 'v']



    # Extraccion de delta p

    if args.onlyPlot == False:
        get_deltaP( [-0.5, -0.25, 0, 0.25, 0.5] )
    

    
    with plt.style.context( ('thesis_classic') ):



        # Lectura y reestructuracion de datos

        dpFile = np.loadtxt('deltaP.dat',unpack=True)

        rdict = {}

        dpdict = {}


        for k in dpFile[0]:

            rdict[k] = []

            dpdict[k] = []


        for k,r,d in zip(dpFile[0],dpFile[1],dpFile[2]):           

            rdict[k].append(r)

            dpdict[k].append(d)



            
        # Grafico para cada kappa        

        for i,kappa in enumerate(rdict.keys()):

            locale.setlocale(locale.LC_NUMERIC, 'es_AR')

            plt.plot( rdict[kappa], dpdict[kappa], linestyle = 'None', marker = mkList[i], mec = colorList[i], label = r'$\kappa={:n}$'.format(kappa))

            gradient,intercept,r_value,p_value,std_err = stats.linregress(rdict[kappa],dpdict[kappa])

            plt.plot( rdict[kappa], [intercept + gradient*x for x in rdict[kappa] ], linestyle = '-', color = 'k')
            




            

        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

        plt.ylabel(r'$\Delta p$', rotation='horizontal', labelpad=15)

        plt.xlabel(r'$1/R$')

        plt.legend( loc='best', numpoints = 1 )
        


        # Guardado

        if args.png == True:

            plt.savefig( 'pressure_kappa.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'pressure_kappa.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()
