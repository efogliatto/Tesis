import vdWColumn as vdw

import vdWColumn.postLBRun as post

import matplotlib.pyplot as plt

import numpy as np

import os

import argparse

import locale






if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de vdWColumn')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
    


    plt.style.use('thesis_classic')



    # Solucion con LBM

    file4 = np.loadtxt( 'c_bar_1.500.dat', unpack = True )

    file5 = np.loadtxt( 'c_bar_1.000.dat', unpack = True )

    file6 = np.loadtxt( 'c_bar_0.500.dat', unpack = True )

    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

    plt.plot( file4[1], file4[2]/300,  linestyle = 'None',  mec = 'r',  marker = 'o', label = r'$\bar{\rho}_r = 1,5$')

    plt.plot( file5[1],  file5[2]/300,  linestyle = 'None',  mec = 'b', marker = 's', label = r'$\bar{\rho}_r = 1,0$')

    plt.plot( file6[1], file6[2]/300, linestyle = 'None', mec = 'g',  marker = '^', label = r'$\bar{\rho}_r = 0,5$')



    # Solucion analitica

    file1 = np.loadtxt( 'BS/c_bar_1.500.dat', unpack = True )
    file2 = np.loadtxt( 'BS/c_bar_1.000.dat', unpack = True )
    file3 = np.loadtxt( 'BS/c_bar_0.500.dat', unpack = True )

    plt.plot( file1[0], file1[3], linestyle = '-', color = 'k')

    plt.plot( file2[0], file2[3], linestyle = '-', color = 'k')

    plt.plot( file3[0], file3[3], linestyle = '-', color = 'k')



    # Labels

    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

    plt.xlabel(r'$T_r$', rotation='horizontal', labelpad=15)

    plt.ylabel(r'$y_0 \, / \, H$')

    plt.legend(loc='best', )
    



    # Guardado

    if args.png == True:

        plt.savefig( 'frac_volumen.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:

        plt.savefig( 'frac_volumen.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
