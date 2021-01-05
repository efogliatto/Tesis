import numpy as np

import matplotlib.pyplot as plt

import os

import argparse

import locale

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)



if __name__ == "__main__":


    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de vdWColumn')

    parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
     
    

    # Perfiles de densidad

    mklist = ['o', 's', '^', '*']        
    
    sp = 300


    # Lectura de datos

    data_300lu = np.loadtxt('300lu.dat', unpack=True)



    # Fuerza

    with plt.style.context( ('thesis_classic') ):
        

        plt.xlabel(r'$y\, / \,H$')

        plt.xlim((0.3, 0.65))

        plt.yticks([0, -2e-03, -4e-03])

        

        
        # Calculo de psi * grad(psi)        
        
        pgp = np.zeros( len(data_300lu[0]) )

        for i in range( len(pgp) ):

            if i == 0:

                pgp[i] = ( data_300lu[4][i+1] - data_300lu[4][i] ) * data_300lu[4][i]

            elif i == len(data_300lu[0]) -1 :

                pgp[i] = ( data_300lu[4][i] - data_300lu[4][i-1] ) * data_300lu[4][i]

            else:

                pgp[i] = ( data_300lu[4][i+1] - data_300lu[4][i-1] ) * data_300lu[4][i] * 0.5





        # Figura

        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

        plt.yticks([0,-0.001,-0.002,-0.003,-0.004])
        
        plt.plot( data_300lu[0] / len(data_300lu[0]), data_300lu[1], label = r'$F_{i_y}$', color='r')

        plt.plot( data_300lu[0] / len(data_300lu[0]), pgp, label = r'$\psi \nabla \psi$', linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
                        
        plt.legend( loc='best' )




        # Guardado

        if args.png == True:

            plt.savefig( 'vdWcolumn_fuerza.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'vdWcolumn_fuerza.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()
