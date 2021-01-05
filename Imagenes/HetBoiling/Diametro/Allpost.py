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
    
    parser = argparse.ArgumentParser(description='Diametro de partida equivalente')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
    
    
    
    with plt.style.context( ('thesis_classic') ):
        

        plt.ylabel(r'$D_{p}$', rotation='horizontal', labelpad=15)

        plt.xlabel(r'$g \, \cdot 10^6 $')

        # plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0), useMathText = True)

        plt.xlim((1.9, 4.1))

        plt.ylim((85, 135))        



        
        
        lbdata = np.loadtxt('d_vs_g.dat', unpack=True)
           
        plt.plot( [g*1e6 for g in lbdata[0]], lbdata[2], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')


        glist = np.linspace(1e-06, 5e-06)

        
        locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
        
        plt.plot( [g*1e6 for g in glist], [0.182*(x**(-0.5)) for x in glist ], linestyle = '-', color = 'r', label = r'$0,182g^{-0,5}$')        
            
        plt.legend( loc='best' )




        # Guardado

        if args.png == True:

            plt.savefig( 'd_vs_g.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'd_vs_g.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()    
