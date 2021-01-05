import vdWColumn as vdw

import vdWColumn.postLBRun as post

import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

from paraview.simple import *

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

    POL.Source.Point1 = [1.0, 0.0, 0.0]

    POL.Source.Point2 = [1.0, xmax, 0.0]

    POL.Source.Resolution = (int)(xmax)


    
    # Alocacion de arreglos

    Array = np.array( range(POL.Source.Resolution+1), dtype=np.float64() )



    # Extraccion del ultimo paso de tiempo

    POL.UpdatePipeline( time = times[-1] )    

    POLf = servermanager.Fetch(POL)
   
    for id in range( POL.Source.Resolution+1 ):
        
        Array[id] = POLf.GetPointData().GetArray(array_name).GetValue(id)

  
    

    return Array






if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de vdWColumn')

    parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()

  


    # Solucion "analitica"    

    Sol = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.8, kappa = 1.0, updateT = True, thcond = 'linear' )
    
    

    # Perfiles de densidad

    colorList = ['r', 'b', 'g', 'y']

    mklist = ['o', 's', '^', '*']

    gridList = [300.0, 600.0, 1200.0, 2400.0]

    lineList = ['-','--',':','-.']
    
    sp = 40

    
    with plt.style.context( ('thesis_classic') ):


        # Analitica

        plt.plot( [Sol[0][np.int(k)] / Sol[0][-1]  for k in np.linspace(0,Sol[3],sp) ], [ Sol[2][np.int(k)] for k in np.linspace(0,Sol[3],sp) ],
                  linestyle = 'None',
                  mec = 'k',
                  marker = 'o',
                  mfc = 'None' )

        plt.plot( [Sol[0][np.int(k)]/Sol[0][-1] for k in np.linspace(Sol[3],len(Sol[0])-1,sp)], [Sol[1][np.int(k)] for k in np.linspace(Sol[3],len(Sol[0])-1,sp)],
                  linestyle = 'None',
                  mec = 'k',
                  marker = 'o',
                  mfc = 'None' )

        
        
        for i, cl in zip( range( args.n + 1 ), colorList ):


            # LB
            
            lbRho = get_array_from_case( case_file = 'Caso{}/lbm.case'.format(i), array_name = 'rho', xmax = gridList[i] )
                       
            plt.plot( [x/(len(lbRho)-1) for x in range(len(lbRho))], [x*12 for x in lbRho], color=cl, label = '{:.0f} u.g.'.format(gridList[i]))





        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

        plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

        # plt.ylim((-0.05,2.05))

        plt.xlim((0.35,0.55))

        plt.xlabel(r'$y \, / \, H$')

        plt.legend( loc='best', numpoints = 1 )
        


        # Guardado

        if args.png == True:

            plt.savefig( 'rhor_vdWColumnHT_grilla.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'rhor_vdWColumnHT_grilla.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()
