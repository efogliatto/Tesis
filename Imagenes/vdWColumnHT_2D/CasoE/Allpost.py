import vdWColumn as vdw

import vdWColumn.postLBRun as post

import numpy as np

import matplotlib.pyplot as plt

import argparse

import os



if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de vdWColumn con conductividad no uniforme')

    parser.add_argument('-n', help='Rango de casos', type = int, default = 0)

    args = parser.parse_args()



    # # Solucion "analitica"    

    # Sol = vdw.rhoNonUniformLambda( Tb = 0.9, Tt = 0.9, kappa = 1.0, updateT = False, thcond = 'linear' )


    
    

    # Perfiles de densidad

    # mkstyle = ['o','^','s','*','x']

    # aList = [0.25, 1, 2]

    # bList = [8, 2, 1]
    
    
    with plt.style.context( ('custom') ):
        

        plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

        # plt.xlabel(r'$E_r \, / \, E_r(H)$')
        plt.xlabel(r'$y \, / \, H$')        



        # # Analitica

        # for k in np.linspace(0,Sol[3],35):
                
        #     plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[2][np.int(k)], linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')

                
        # for k in np.linspace(Sol[3],len(Sol[0])-1,35):
                
        #     plt.plot( Sol[0][np.int(k)] / Sol[0][-1], Sol[1][np.int(k)],  linestyle = 'None', color = 'k', marker = 'o', mfc = 'None')
        


        # Solucion LBM
            
        for i in range( args.n + 1 ):

            os.chdir('Caso{}'.format(i))

            os.system('pvpython GetData.py')

            os.chdir('../')

            lbData = np.genfromtxt('Caso{}/Caso.csv'.format(i), delimiter=',', unpack = True)[0][1:]

            Er = [x/(len(lbData)-1) for x in range(len(lbData))]

            rhor = [x*12 for x in lbData]


            if i < 4:
            
                plt.plot( Er, rhor )

            else:

                j = i - 4

                rhor = [x*3*bList[j] for x in lbData]

                plt.plot( Er[::3], rhor[::3], linestyle = 'None', color = 'k', marker = mkstyle[j], mfc = 'None')


            
            
        # plt.legend( loc='best' )

        plt.xlim((0.30,0.65))

        plt.savefig( 'rho_r.eps', format='eps', dpi=600 )

        plt.gcf().clear()







    # Ancho de interfase
    
    with plt.style.context( ('custom') ):

        
        plt.xlabel(r'e (l.u.)')        

        plt.xlabel(r'$y \, / \, H$')


        lu = []

        eps = []

        

        # Solucion LBM
            
        for i in range( args.n + 1 ):

            os.chdir('Caso{}'.format(i))

            os.system('pvpython GetData.py')

            os.chdir('../')

            lbData = np.genfromtxt('Caso{}/Caso.csv'.format(i), delimiter=',', unpack = True)[0][1:]

            xcross, ll, rl = post.interphase( lbData )

            lu.append( len(lbData) - 1 )

            eps.append(rl - ll)
            


        plt.plot( lu, eps, linestyle = '-', marker = 'o' )            
                        
        plt.savefig( 'intWidth.eps', format='eps', dpi=600 )

        plt.gcf().clear()
        
