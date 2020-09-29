import vdWColumn as vdw

import vdWColumn.postLBRun as post

import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

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

    parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()

  


    # Solucion "analitica"    

    TbList = [0.9, 0.8, 0.7, 0.6]

    Sol = []
    
    for i in range( args.n + 1 ):
        
        Sol.append( vdw.rhoNonUniformLambda( Tt = 0.99, Tb = TbList[i], kappa = 1.0, updateT = True, thcond = 'linear' ) )


    
    

    # Perfiles de densidad

    colorList = ['r', 'b', 'g', 'y']

    mklist = ['o', 's', '^', '*']    
    
    sp = 15

    
    with plt.style.context( ('../../thesis_classic.mplstyle') ):
      

        for i, mk in zip( range( args.n + 1 ), mklist ):


            # Analitica

            label = r'$T_b={:.1f} \, T_c$'.format(TbList[i])

            plt.plot( [Sol[i][0][np.int(k)] / Sol[i][0][-1]  for k in np.linspace(0,Sol[i][3],sp) ], [ Sol[i][2][np.int(k)] for k in np.linspace(0,Sol[i][3],sp) ],
                      linestyle = 'None',
                      mec = colorList[i],
                      marker = mk,
                      mfc = 'None',
                      mew=1.5,
                      label = label )

            plt.plot( [Sol[i][0][np.int(k)]/Sol[i][0][-1] for k in np.linspace(Sol[i][3],len(Sol[i][0])-1,sp)], [Sol[i][1][np.int(k)] for k in np.linspace(Sol[i][3],len(Sol[i][0])-1,sp)],
                      linestyle = 'None',
                      mec = colorList[i],
                      marker = mk,
                      mfc = 'None',
                      mew=1.5)
            
                                     

            # LB
            
            lbRho = get_array_from_case( case_file = 'Caso{}/lbm.case'.format(i), array_name = 'rho', xmax = 300.0 )
                       
            plt.plot( [x/300 for x in range(len(lbRho))], [x*12 for x in lbRho], linestyle = '-', color='k')





        # Ejes y leyenda

        plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

        plt.ylim((-0.15,2.65))

        plt.xlabel(r'$y \, / \, H$')

        plt.legend( loc='best', numpoints = 1 )
        


        # Guardado

        if args.png == True:

            plt.savefig( 'rhor_vdWcolumnHT.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'rhor_vdWcolumnHT.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()





    with plt.style.context( ('../../thesis_classic.mplstyle') ):

        
        sp = 30
      

        for i, mk in zip( range( args.n + 1 ), mklist ):


            # Analitica

            label = r'$T_b={:.1f} \, T_c$'.format(TbList[i])

            plt.plot( [Sol[i][0][np.int(k)] / Sol[i][0][-1] for k in np.linspace(0,len(Sol[i][0])-1,sp) ], [ Sol[i][4][np.int(k)] for k in np.linspace(0,len(Sol[i][0])-1,sp) ],
                      linestyle = 'None',
                      mec = colorList[i],
                      marker = mk,
                      mfc = 'None',
                      mew=1.5,
                      label = label )
            
                                     

            # LB
            
            lbT = get_array_from_case( case_file = 'Caso{}/lbm.case'.format(i), array_name = 'T', xmax = 300.0 )
                       
            plt.plot( [x/300 for x in range(len(lbT))], [x*27 for x in lbT], linestyle = '-', color='k')





        # Ejes y leyenda

        plt.ylabel(r'$T_r$', rotation='horizontal', labelpad=15)

        plt.ylim((0.57,1.03))

        plt.xlabel(r'$y \, / \, H$')

        plt.legend( loc='lower right', numpoints = 1 )
        


        # Guardado

        if args.png == True:

            plt.savefig( 'Tr_vdWcolumnHT.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'Tr_vdWcolumnHT.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()
        
