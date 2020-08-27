import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import MaxwellConstruction as mx
import collections
import argparse


if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Ejemplo de construccion de Maxwell con vdW')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')    

    args = parser.parse_args()    

    

    
    # Ecuacion de VdW

    vdw = mx.EOS('VanDerWaals')


    
    # Coexistencia en Tr = 0.95
    
    Vrmin,Vrmax,Vr,pr,pr0 = mx.coex_only_for_plot(vdw, 0.95, Vspace=(0.57,2,300))


    

    # Grafico de EOS y zonas sombreadas

    plt.style.use('../thesis_classic.mplstyle')

    fig = plt.figure()
    
    ax = fig.gca()


    ax.plot(Vr, pr, linewidth=2, color='r')
    
    ax.axhline(pr0)

    Vrslice = []

    prslice = []

    for i in range(len(Vr)):

        if (Vr[i]>=Vrmin) and (Vr[i]<=Vrmax):

            Vrslice.append(Vr[i])

            prslice.append(pr[i])
        
        
    ax.fill_between(Vrslice, pr0, prslice, interpolate=True, alpha=0.3)




    # Nombres de las regiones
    
    ax.text(0.79,0.78,'A',fontsize=18)

    ax.text(1.31,0.822,'B',fontsize=18)    



    
    
    # Volumenes de cada fase

    ax.vlines(x=Vrmin, ymin=0.7, ymax=pr0, linestyles='dashed', lw=1)

    ax.vlines(x=Vrmax, ymin=0.7, ymax=pr0, linestyles='dashed', lw=1)    



    # Ejes

    ax.set_xlabel(r'$v$')

    ax.set_ylabel(r'$p$', rotation='horizontal', labelpad=15)
    
    ax.set_ylim((0.7,1.0))


    

    # Ticks especificos

    x_formatter = FixedFormatter(['$v_l$', '$v_g$'])

    x_locator = FixedLocator([Vrmin,Vrmax])

    ax.xaxis.set_major_formatter(x_formatter)

    ax.xaxis.set_major_locator(x_locator)
    
    
    y_formatter = FixedFormatter([r'$p_0$'])

    y_locator = FixedLocator([pr0])

    ax.yaxis.set_major_formatter(y_formatter)

    ax.yaxis.set_major_locator(y_locator)
    
    


    # Export

    if args.png == True:

        fig.savefig( 'vdW_Maxwell.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:
        
        fig.savefig( 'vdW_Maxwell.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )
