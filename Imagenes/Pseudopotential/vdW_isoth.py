import numpy as np

import matplotlib.pyplot as plt

import argparse




if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Ejemplo de construccion de Maxwell con vdW')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')    

    args = parser.parse_args()

    
    

    # Volumen molar

    vmol = np.linspace(0.4,5,300)


    # Presion reducida

    def pr(Tr, v):

        return (8.*Tr) / (3.*v -1.) - 3./(v*v)



    # Estilo

    plt.style.use('../thesis_classic.mplstyle')
    
    
    # Isoterma critica

    plt.plot( vmol, [pr(1,v) for v in vmol], color='k', linewidth=2 )


    # Isotermas supercriticas<

    for Tr in np.linspace(1.1,2.5,10):

        plt.plot( vmol, [pr(Tr,v) for v in vmol], color='r', linewidth=1 )


    # Isotermas subcriticas<        

    for Tr in np.linspace(0.6,0.9,5):

        plt.plot( vmol, [pr(Tr,v) for v in vmol], color='b', linewidth=1 )        


  

    plt.tick_params( axis='x', which='both', bottom=False, top=False,  labelbottom=False)

    plt.tick_params( axis='y', which='both', left=False, right=False,  labelleft=False)

    plt.ylim((-3,4))

    plt.xlim((0.35,5.7))    

    plt.ylabel(r'$p$', rotation='horizontal', labelpad=15)

    plt.xlabel(r'$v$')

    plt.xscale('log')


    if args.png == True:

        plt.savefig( 'vdW_isoth.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:

        plt.savefig( 'vdW_isoth.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )



    plt.gcf().clear()
