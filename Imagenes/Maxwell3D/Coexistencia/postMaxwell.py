import os

import numpy as np

import matplotlib.pyplot as plt

import argparse

import collections

import glob

import MaxwellConstruction as mx

from paraview.simple import *






if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución del problema de construcción de Maxwell para diferentes constantes')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')    

    args = parser.parse_args()
    

    
    # Estilo

    plt.style.use('../../thesis_classic.mplstyle')

    colorList = ['r', 'b', 'g', 'y']

    mkList = ['o', 's', '^', '*']   

    

    # Lista con parametros

    # paramList = [ [0.5, 4.0, 1.25],
    #               [0.5, 4.0, 0.125],                  
    #               [0.5, 4.0, 0.0125] ]
    paramList = [ [0.5, 4.0, 0.125] ]
    


    # Directorio del caso y limpieza
    
    main_dir = os.getcwd()   

    


    # Movimiento en todos los parametros
    
    for i,param in enumerate(paramList):


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

            
            # Carga del caso

            lbmcase = EnSightReader( CaseFileName = fname + '/lbm.case')

            times = lbmcase.TimestepValues

            lbmcase.PointArrays = ['rho']

            

            # Ultimo paso de tiempo

            lbmcase.UpdatePipeline( times[-1] )

            

            # Valores maximos

            extrema = lbmcase.PointData.GetArray('rho').GetRange()


            # Listas para graficos

            TList.append(Tr)

            vdw = mx.EOS( 'VanDerWaals', a = param[0], b = param[1] )
            
            rhogList.append( extrema[0]/vdw.rhoc() )

            rholList.append( extrema[1]/vdw.rhoc() )            




        plt.plot( rhogList,
                  TList,
                  label = r'$\sigma={}$'.format(param[2]),
                  linestyle = 'None',
                  mec = colorList[i],
                  marker = mkList[i],
                  mfc = 'None')

        plt.plot( rholList,
                  TList,
                  linestyle = 'None',
                  mec = colorList[i],
                  marker = mkList[i],
                  mfc = 'None')






    # Curva de coexistencia de Van Der Waals


    def ordToList( dict ):
    
        col = collections.OrderedDict(sorted(dict.items()))

        x = []
        
        y = []
    
        for k,v in col.items():

            x.append(k)
            y.append(v)

        return x,y


    

    TEos = np.concatenate( [np.arange(0.5,0.925,0.025) , np.array([0.925, 0.94, 0.95, 0.975, 0.98, 0.99, 0.9925, 0.995]) ] )

    vdw = mx.EOS('VanDerWaals')

    coex = {1:1}

    for i,T in enumerate(TEos):

        step = 0.999
        if T < 0.6:
            step = 0.9999

        Vrmin,Vrmax = mx.coexistencia(vdw, T, plotPV=False, step_size=step)

        coex[1/Vrmin] = T
        coex[1/Vrmax] = T

    coex = ordToList( collections.OrderedDict(sorted(coex.items())) )

    plt.plot(coex[0], coex[1], label='van der Waals', color='k')
        


    plt.ylabel(r'$T/T_c$')

    plt.xlabel(r'$\rho/\rho_c$')

    plt.xscale('log')

    plt.legend(loc = 'best', framealpha=1)


    
    if args.png == True:

        plt.savefig( 'vdW_sigma.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:
        
        plt.savefig( 'vdW_sigma.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )

          

    plt.gcf().clear()

        


    


    
