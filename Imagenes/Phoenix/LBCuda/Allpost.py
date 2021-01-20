import numpy as np

import matplotlib.pyplot as plt

import argparse

import os

import locale



if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Graficos de SpeedUp')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()


    

    # Resultados de Thomas

    bins = [r'$2^8$', r'$2^{10}$', r'$2^{12}$', r'$2^{14}$', r'$2^{16}$', r'$2^{18}$', r'$2^{20}$', r'$2^{22}$']

    SimpleList = [1.31, 4.53, 10.401, 13.613, 16.679, 18.394, 18.613, 18.65]

    DoubleList = [1.123, 3.725, 8.174, 9.397, 10.33, 10.932, 10.977, 11.44]

   
    with plt.style.context( ('thesis_classic') ):
      

        # Grafico
        
        plt.bar( bins, SimpleList, width=0.4, color = 'r', align = 'center' )
            


        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
        
        plt.ylabel(r'SpeedUp')

        plt.xlabel(r'Cantidad de nodos de la malla')


        # Guardado

        if args.png == True:

            plt.savefig( 'lbcuda_760_simple.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'lbcuda_760_simple.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()




    with plt.style.context( ('thesis_classic') ):
      

        # Grafico
        
        plt.bar( bins, DoubleList, width=0.4, color = 'r', align = 'center' )
            


        # Ejes y leyenda

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
        
        plt.ylabel(r'SpeedUp')

        plt.xlabel(r'Cantidad de nodos de la malla')


        # Guardado

        if args.png == True:

            plt.savefig( 'lbcuda_760_doble.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'lbcuda_760_doble.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()
        
