import vdWColumn as vdw

import vdWColumn.postLBRun as post

import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

from paraview.simple import *

import stefanFlow as stf

import matplotlib.ticker as mticker

import locale




# Extraccion de arreglos en linea desde el centro (xmax/2) hasta xmax

def get_array_from_case( lbmcase, time, array_name = 'rho', xmax = 600.0 ):


    # Carga del caso con arrays para rho y p
    
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

    POL.UpdatePipeline( time )    

    POLf = servermanager.Fetch(POL)
   
    for id in range( POL.Source.Resolution+1 ):
        
        Array[id] = POLf.GetPointData().GetArray(array_name).GetValue(id)

  
    

    return Array





if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Post procesamiento del frente de evaporación')

    parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()




    # Propiedades de la solucion analitica

    Tw = [0.0682597, 0.0727599, 0.0772602]

    dxi = [15, 7, 6]

    aa = 1

    bb = 4

    cv = 4


    Tc = 8.0 * aa / (27. * bb)

    Tr = 0.8

    q3 = 1.8

    alpha1 = -1

    alpha2 = 1


       

    # Perfiles de densidad

    colorList = ['r', 'b', 'g', 'y']

    mklist = ['o', 's', '^', '*']    

    
    
    with plt.style.context( ('thesis_classic') ):
      

        for i, mk in zip( range( args.n + 1 ), mklist ):



            # Solucion LB

            lbmcase = EnSightReader( CaseFileName='Caso{}/lbm.case'.format(i) )

            times = lbmcase.TimestepValues

            xint = []


            for t in times:

                if t != 0.0:

                    lbRho = get_array_from_case( lbmcase, t, array_name = 'rho', xmax = 600.0 )

                    xcross, ll, rl = post.interphase( lbRho )

                    xint.append(xcross)

                else:

                    xint.append( dxi[i]  )

                

            plt.plot( [t/1e6 for t in times], [(x-dxi[i])/600 for x in xint], linestyle='-', color='k' )
            




            # Solucion analitica

            hl, hg = vdw.latentHeat(Tr*Tc, aa, bb)       

            St = cv * (Tw[i] - Tr*Tc) / (hg - hl)

            beta = stf.betaConstant(St, 0.)

            alpha = (1./q3 - 0.5)*( 4. + 3.*alpha1 + 2.*alpha2) / 6.

            tplot = times[0::2]

            locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
            
            plt.plot( [t/1e6 for t in tplot], [ 2 * beta * (alpha**0.5) * (t**0.5015) / 600  for t in tplot],
                      linestyle = 'None',
                      mec = colorList[i],
                      marker = mk,
                      mfc = 'None',                      
                      label = r'$St = {:.1n}$'.format(St))            
            


            


        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

        plt.ylabel(r'$x_i \, / \, L$')

        plt.xlabel(r'$t \, \cdot 10^{-6}$')            

        plt.legend( loc='best', numpoints = 1 )
        


        # Guardado

        if args.png == True:

            plt.savefig( 'Stefan_m1_1.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'Stefan_m1_1.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()
