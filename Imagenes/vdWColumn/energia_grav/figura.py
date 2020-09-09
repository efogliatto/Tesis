import os

import vdWColumn as vdw

import vdWColumn.postLBRun as post

import matplotlib.pyplot as plt

import numpy as np

import argparse






if __name__ == "__main__":


    
    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución de vdWColumn')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')        

    args = parser.parse_args()
    


    plt.style.use('../../thesis_classic.mplstyle')




    # van Der Waals properties

    b = 4.0

    mkstyle = ['o','s','^', '*','x']


    
    plt.figure()
    
    
    # Move over Caso folders

    for i, et in zip( range(3), [1.0e-01, 1.0e-02, 1.0e-03, 1.0e-04] ):


        # Solucion LB
                              
        rho = np.loadtxt( 'rho_{}'.format(i) )

        intm, ll, rl = post.interphase( rho, width = 0.05 )
        
        plt.plot( [  (z-intm)/(len(rho)-1) for z in range( len(rho) )  ],  rho * 3.0 * b, linestyle = '-')




        # Solucion analitica

        sp = 200
        
        Er, Cg, Cl, Ei, Tr = vdw.rhoNonUniformLambda( Tt = 0.99, Tb = 0.99, Et = et )

        plabel = "$E_r=10^{" + "{}".format(-1-i) + "}$"
        
        plt.plot( [ (z-Er[Ei]) / et  for z in Er[Ei::-sp] ], Cl[Ei::-sp], linestyle = 'None', color = 'k',  marker = mkstyle[i],  mfc = 'None', label = plabel)

        plt.plot( [ (z-Er[Ei]) / et  for z in Er[Ei::sp] ], Cg[Ei::sp], linestyle = 'None', color = 'k',  marker = mkstyle[i],  mfc = 'None')        
                  
        


        

    # Labels

    plt.ylabel(r'$\rho_r$', rotation='horizontal', labelpad=15)

    plt.xlabel(r'$(y - y_0)\, / \,H$')

    plt.xlim((-0.4,0.4))

    # plt.legend(loc='best')


    dirname = os.path.basename( os.getcwd() )
    
    plt.savefig( 'fig_' + dirname + '.eps', format='eps', dpi=300 )

    plt.savefig( 'fig_' + dirname + '.jpg', format='jpg', dpi=300 )        
