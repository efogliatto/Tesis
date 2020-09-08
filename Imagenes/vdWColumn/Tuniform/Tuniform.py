import vdWColumn as vdw

import matplotlib.pyplot as plt

import numpy as np

# import argparse

import os



if __name__ == "__main__":


    # # Argumentos de consola
    
    # parser = argparse.ArgumentParser(description='Resolución de vdWColumn con conductividad no uniforme')

    # parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    # args = parser.parse_args()


    # Temperatura uniforme
    
    with plt.style.context( ('custom') ):


        # Diccionario de casos
        Casos = { 0.99 : 0,
                  0.9  : 1,
                  0.8  : 2 }


        # Solucion "analitica"    

        Sol = []
    
        for T in Casos.keys():
        
            Sol.append( vdw.rhoNonUniformLambda( Tt = T, Tb = T, Et = 0.01 ) )



        # Perfiles de densidad

        mkstyle = ['o','^','s','*','x']
    
        

        # plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)
        plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

        plt.xlabel(r'$E_r \, / \, E_r(H)$')


        for T in Casos.keys():


            # Analitica

            i = Casos[T]

            Ei = Sol[i][3]

            mk = mkstyle[i]               

            # plt.plot( Sol[i][0][Ei::-sp] / Sol[i][0][-1], Sol[i][2][Ei::-sp], linestyle = 'None', color = 'k', marker = mk, mfc = 'None')

            # plt.plot( Sol[i][0][Ei::sp] / Sol[i][0][-1], Sol[i][1][Ei::sp],  linestyle = 'None', color = 'k', marker = mk, mfc = 'None')


            sp = np.linspace(0,Ei,15)

            for k in sp:

                if k == 0:
                
                    plt.plot( Sol[i][0][np.int(k)] / Sol[i][0][-1], Sol[i][2][np.int(k)], linestyle = 'None', color = 'k', marker = mk, mfc = 'None', label = 'Tr = {}'.format(T))

                else:

                    plt.plot( Sol[i][0][np.int(k)] / Sol[i][0][-1], Sol[i][2][np.int(k)], linestyle = 'None', color = 'k', marker = mk, mfc = 'None')


            sp = np.linspace(Ei,len(Sol[i][0])-1,15)

            for k in sp:
                
                plt.plot( Sol[i][0][np.int(k)] / Sol[i][0][-1], Sol[i][1][np.int(k)],  linestyle = 'None', color = 'k', marker = mk, mfc = 'None')
            

                

            # Solucion con LBM

            os.chdir('Caso{}'.format(i))

            os.system('pvpython GetData.py')

            os.chdir('../')

            lbData = np.genfromtxt('Caso{}/Caso.csv'.format(i), delimiter=',', unpack = True)[0][1:]

            plt.plot( [x/600 for x in range(len(lbData))], [x*12 for x in lbData], linestyle = '-' )

            
            
            
        plt.legend( loc='best' )

        plt.savefig( 'Tuniform.eps', format='eps', dpi=600 )

        plt.gcf().clear()        
