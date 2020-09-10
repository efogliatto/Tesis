import os

import vdWColumn as vdw

import vdWColumn.postLBRun as post

import matplotlib.pyplot as plt

import numpy as np

import argparse

from paraview.simple import *



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

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
    


    # Estilo
    
    plt.style.use('../../thesis_classic.mplstyle')



    # van Der Waals properties

    b = 4.0

    mkstyle = ['o','s','^', '*','x']



    # Colores y espaciado

    colorList = ['r', 'b', 'g', 'y']

    mkList = ['o', 's', '^', '*']

    sp = 15


    # Lista de energias

    EtList = [1.0e-01, 1.0e-02, 1.0e-03]



    # Soluciones analiticas

    Sol = []
    
    for et in EtList:

        Sol.append( vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.99, kappa = 1.0, updateT = False, thcond = 'linear', Et = et ) )
    
       
    
    # Move over Caso folders

    for i, et in enumerate( EtList ):        


        # Solucion LB
                              
        rho = get_array_from_case( case_file = 'Caso{}/lbm.case'.format(i), array_name = 'rho', xmax = 300.0 )

        intm, ll, rl = post.interphase( rho, width = 0.05 )
        
        plt.plot( [  (z-intm)/(len(rho)-1) for z in range( len(rho) )  ],  rho * 3.0 * b, linestyle = '-', color='k')




        # Solucion analitica

        label = "$E_r=10^{" + "{}".format(-1-i) + "}$"
      
        plt.plot( [ (Sol[i][0][np.int(k)] - Sol[i][0][Sol[i][3]]) / Sol[i][0][-1]  for k in np.linspace(0,Sol[i][3],sp) ], [ Sol[i][2][np.int(k)] for k in np.linspace(0,Sol[i][3],sp) ],
                  linestyle = 'None',
                  mec = colorList[i],
                  marker = mkList[i],
                  mfc = 'None',
                  label = label )

        plt.plot( [ (Sol[i][0][np.int(k)] - Sol[i][0][Sol[i][3]]) / Sol[i][0][-1] for k in np.linspace(Sol[i][3],len(Sol[i][0])-1,sp)], [Sol[i][1][np.int(k)] for k in np.linspace(Sol[i][3],len(Sol[i][0])-1,sp)],
                  linestyle = 'None',
                  mec = colorList[i],
                  marker = mkList[i],
                  mfc = 'None')

        

    # Labels

    plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

    plt.xlabel(r'$(y - y_0)\, / \,H$')

    plt.xlim((-0.4,0.4))

    plt.legend(loc='best')



    # Guardado

    if args.png == True:

        plt.savefig( 'rhor_energia_grav.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:

        plt.savefig( 'rhor_energia_grav.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

    plt.gcf().clear()    
