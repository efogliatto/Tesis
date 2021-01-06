import numpy as np
import CoolProp.CoolProp as CP
import CoolProp.Plots as CPP
import matplotlib.pyplot as plt
import MaxwellConstruction as mx
import collections
import argparse
import locale


if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='EOS para fluidos definidos en CoolProp')

    parser.add_argument('-w', help='Excentricidad', type = float, default = 0.344)

    parser.add_argument('-svg', help='Imagen en formato svg', action='store_true')    

    args = parser.parse_args()    


    # Estilo

    plt.style.use('thesis_classic')

    
    # Propiedades criticas

    plt.plot(1620.0 / 557.7, 0.73474, linestyle='None', color='r', marker='o', label='FC-72', mec='k')
    plt.plot(13.4 / 557.7, 0.73474, linestyle='None', color='r', marker='o', mec='k')
    
    
    

    def ordToList( dict ):
    
        col = collections.OrderedDict(sorted(dict.items()))

        x = []
        
        y = []
    
        for k,v in col.items():

            x.append(k)
            y.append(v)

        return x,y  


    TEos = np.concatenate( [np.arange(0.6,0.925,0.025) , np.array([0.925, 0.95, 0.975, 0.99, 0.995]) ] )
    # TEos = np.linspace(0.5,0.99,50)

    # Curva de coexistencia de Van Der Waals

    vdw = mx.EOS('VanDerWaals')

    coex = {1:1}

    for i,T in enumerate(TEos):

        step = 0.999
        if T < 0.6:
            step = 0.9999

        Vrmin,Vrmax = mx.coexistencia(vdw, T, plotPV=False, step_size=step)

        coex[1/Vrmin] = T
        coex[1/Vrmax] = T

    coex = ordToList( collections.OrderedDict(sorted(coex.items())) )

    plt.plot(coex[0], coex[1], label='van der Waals')





    # Curva de coexistencia de Carnahan-Starling

    cs = mx.EOS('Carnahan-Starling')

    coex = {1:1}

    for i,T in enumerate(TEos):    

        step = 0.999
        if T < 0.6:
            step = 0.9999
    
        Vrmin,Vrmax = mx.coexistencia(cs, T, plotPV=False, Vspace=(0.2,500,100000), step_size=step)

        coex[1/Vrmin] = T
        coex[1/Vrmax] = T

    coex = ordToList( collections.OrderedDict(sorted(coex.items())) )

    plt.plot(coex[0], coex[1], label='Carnahan-Starling')




    # Curva de coexistencia de Peng-Robinson

    prob = mx.EOS('Peng-Robinson', w = args.w)

    coex = {1:1}

    for i,T in enumerate(TEos):    

        step = 0.999
        if T < 0.6:
            step = 0.9999
        
    
        if T >= 0.8:
            Vrmin,Vrmax = mx.coexistencia(prob, T, plotPV=False, Vspace=(0.3,50,10000), step_size=step)

        else:
            Vrmin,Vrmax = mx.coexistencia(prob, T, plotPV=False, Vspace=(0.28,4000,200000), step_size=step)        

        coex[1/Vrmin] = T
        coex[1/Vrmax] = T

    coex = ordToList( collections.OrderedDict(sorted(coex.items())) )

    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
    
    plt.plot(coex[0], coex[1], label=r'Peng-Robinson ($\omega$={:n})'.format(args.w))

    

    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
    
    plt.ylabel(r'$T/T_c$')

    plt.xlabel(r'$\rho/\rho_c$')

    plt.xscale('log')

    plt.legend(loc = 'best', framealpha=1)

    # plt.grid()

    # plt.rcParams['figure.dpi'] = 150

    # plt.show()

    # plt.draw()



    if args.svg == True:

        plt.savefig( 'EOS_FC72.svg', format='svg', bbox_inches = 'tight', dpi=600 )

    else:
        
        plt.savefig( 'EOS_FC72.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )

          

    plt.gcf().clear()

    # plt.ioff()
