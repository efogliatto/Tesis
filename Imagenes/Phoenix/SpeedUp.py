import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

from scipy import stats

import matplotlib.ticker as mticker

import locale



if __name__ == "__main__":


    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='SpeedUp')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
    
    
    
    with plt.style.context( ('thesis_classic') ):
        

        # Teorico

        plt.plot( range(20,321), [n/20. for n in range(20,321)], linestyle = '-', color = 'k', label='Teórico')


        
        # Infiniband

        cores = range(20,321,20)
        
        infiniband = [1, 2, 3, 4, 5, 6, 7, 8, 8.92, 9.9, 10.89, 11.85, 12.83, 13.8, 14.78, 15.76] 
           
        plt.plot( cores, infiniband, linestyle = 'None', color = 'r', marker = 'o', mfc = 'None', mec='r', label='Infiniband')



        # Ethernet

        ethernet = [1, 2, 3, 4, 5, 5.75, 6.4, 7, 7.4, 7.8, 8.2, 8.5, 8.8, 9.1, 9.4, 9.6] 
           
        plt.plot( cores, ethernet, linestyle = 'None', color = 'b', marker = 's', mfc = 'None', mec='b', label='Ethernet')


            

        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

        plt.ylabel(r'$t_r/t_c$')

        plt.xlabel('Núcleos')       

        plt.legend( loc='best' )
        


        # Guardado

        if args.png == True:

            plt.savefig( 'SpeedUp.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'SpeedUp.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()    
