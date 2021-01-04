import numpy as np
import matplotlib.pyplot as plt
import MaxwellConstruction as mx
import collections
import argparse
import locale


if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='EOS para fluidos definidos en CoolProp')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')    

    args = parser.parse_args()    

    
    

    def ordToList( dict ):
    
        col = collections.OrderedDict(sorted(dict.items()))

        x = []
        
        y = []
    
        for k,v in col.items():

            x.append(k)
            y.append(v)

        return x,y



    # Estilo

    plt.style.use('../../thesis_classic.mplstyle')
    


    TEos = np.concatenate( [np.arange(0.5,0.925,0.025) , np.array([0.925, 0.94, 0.95, 0.975, 0.98, 0.99, 0.9925, 0.995]) ] )
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

    plt.plot(coex[0], coex[1], label='van der Waals', color='k')







    # Solucion con LBM

    sigma_0 = np.loadtxt( "sigma_1.25.dat", unpack = True )

    sigma_1 = np.loadtxt( "sigma_0.125.dat", unpack = True )

    sigma_2 = np.loadtxt( "sigma_0.0125.dat", unpack = True )



    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
    
    plt.plot( sigma_0[4],
              sigma_0[1],
              label = r'$\sigma=1.25$',
              linestyle = 'None',
              mec = 'r',
              marker = 'o',
              mfc = 'None')

    plt.plot( sigma_0[5],
              sigma_0[1],
              linestyle = 'None',
              mec = 'r',
              marker = 'o',
              mfc = 'None')

    plt.plot( sigma_1[4],
              sigma_1[1],
              label = r'$\sigma=0.125$',
              linestyle = 'None',
              mec = 'b',
              marker = '^',
              mfc = 'None')

    plt.plot( sigma_1[5],
              sigma_1[1],
              linestyle = 'None',
              mec = 'b',
              marker = '^',
              mfc = 'None')

    plt.plot( sigma_2[4],
              sigma_2[1],
              label = r'$\sigma=0.0125$',
              linestyle = 'None',
              mec = 'g',
              marker = 's',
              mfc = 'None')

    plt.plot( sigma_2[5],
              sigma_2[1],
              linestyle = 'None',
              mec = 'g',
              marker = 's',
              mfc = 'None')
    




    
    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")

    plt.ylabel(r'$T/T_c$')

    plt.xlabel(r'$\rho/\rho_c$')

    # plt.xscale('log')

    plt.legend(loc = 'best', framealpha=1)

    # plt.grid()

    # plt.rcParams['figure.dpi'] = 150

    # plt.show()

    # plt.draw()



    if args.png == True:

        plt.savefig( 'vdW_sigma.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:
        
        plt.savefig( 'vdW_sigma.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )

          

    plt.gcf().clear()

    # plt.ioff()
