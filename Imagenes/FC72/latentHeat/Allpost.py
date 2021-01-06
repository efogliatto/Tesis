import vdWColumn as vdw

import vdWColumn.postLBRun as post

import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

from scipy import stats

import matplotlib.ticker as mticker

import locale



if __name__ == "__main__":


    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Calor latente')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
    
    
    
    with plt.style.context( ('thesis_classic') ):
      
        

        # Datos de LB ya procesados       
        
        lbdata = np.loadtxt('lheat.dat', unpack=True)

        plt.plot( [m*1e8 for m in lbdata[1]], [q*1e8 for q in lbdata[0]], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')



        # Ajuste

        qlist = np.linspace(1e-08, 5e-08)
       
        plt.plot( [q*1e8/0.26 for q in qlist], [q*1e8 for q in qlist], linestyle = '-', color = 'r', label = r'$h_{fg}=0,26$')        



        
        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
                
        plt.ylabel('$q$' + '\"' + '$\, \cdot 10^8$')

        plt.xlabel('$m$' + '\"' + '$\, \cdot 10^8$')

        plt.yticks([1, 2, 3, 4, 5])
        
        plt.legend( loc='best' )




        # Guardado

        if args.png == True:

            plt.savefig( 'latentHeat.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'latentHeat.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()    
