import numpy as np

import matplotlib.pyplot as plt

import os

import argparse



if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de vdWColumn')

    parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()    
     
    

    # Perfiles de densidad

    mkstyle = ['o', 's', '^', '*']
    
    sp = 300


    # Lectura de datos

    data_300lu = np.loadtxt('300lu.dat', unpack=True)



    # Terminos de ecuacion macro

    with plt.style.context( ('../../thesis_classic.mplstyle') ):



        def align_yaxis(ax1, v1, ax2, v2):
            """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
            _, y1 = ax1.transData.transform((0, v1))
            _, y2 = ax2.transData.transform((0, v2))
            inv = ax2.transData.inverted()
            _, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
            miny, maxy = ax2.get_ylim()
            ax2.set_ylim(miny+dy, maxy+dy)



        
        # Subplots

        fig, ax1 = plt.subplots()    
        

        
        # Figura 1

        ax1.set_ylabel(r'$F_{int_y}$, $\partial_y (\rho c_s^2)$')

        ax1.set_ylim((-4.25e-03, 1.25e-03))

        ax1.set_xlabel(r'$y\,/\,H$')

        ax1.set_xlim((0.3, 0.65))

        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText = True)

        ax1.set_yticks([0, -2e-03, -4e-03])

        ax1.plot( data_300lu[0]/ len(data_300lu[0]), data_300lu[1], label = r'$F_y$', color='r')

        ax1.plot( data_300lu[0][::2]/ len(data_300lu[0]), data_300lu[7][::2]/3, label = r'$\partial_y (\rho c_s^2)$', linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')


        # Figura 2

        ax2 = ax1.twinx()

        ax2.set_ylabel(r'$2 G^2 c^4 \sigma \partial_y \left( |\partial_y \psi|^2 \right)$, $F_{b_y}$')        

        ax2.set_xlim((0.3, 0.65))

        ax2.set_ylim((-1.5e-04, 0.2e-04))

        ax2.set_yticks([0, -0.6e-04, -1.2e-04])

        ax2.ticklabel_format(style='sci', axis='y', scilimits=(0,0), useMathText = True)

        ax2.plot( data_300lu[0]/ len(data_300lu[0]), data_300lu[6]*2*0.125, label = r'$2 G^2 c^4 \sigma \partial_z \left( |\partial_z \psi|^2 \right)$', linestyle = '--')

        ax2.plot( data_300lu[0]/ len(data_300lu[0]), data_300lu[3]*(-1.234567e-07), label = r'$F_b$', linestyle = ':')
        
        # ax2.plot( data_300lu[0]/ len(data_300lu[0]), data_300lu[9], label = 'Residuo', linestyle = ':')
        

        
                        
        # fig.legend( loc='center right' )

        align_yaxis(ax1, 0, ax2, 0)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped



        
        # Guardado

        if args.png == True:

            plt.savefig( 'vdWcolumn_fuerza_comp.png', format='png', bbox_inches = 'tight', dpi=600 )

        else:

            plt.savefig( 'vdWcolumn_fuerza_comp.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
       

        plt.gcf().clear()

