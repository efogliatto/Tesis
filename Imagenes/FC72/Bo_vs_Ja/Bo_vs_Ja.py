import numpy as np
import matplotlib.pyplot as plt
import argparse
import locale


if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Comparacion con datos de Hutter. Bo vs Ja')

    parser.add_argument('-png', help='Imagen en formato png', action='store_true')    

    args = parser.parse_args()    



    # Estilo

    plt.style.use('thesis_classic')

    

    # Datos experimentales

    hutter = np.loadtxt('D_vs_supheat.dat', unpack=True)

    rho_l = 1620

    g = 9.81

    sigma_s = 0.00827

    cv = 1098

    hfg = 84500  

    # plt.errorbar(hutter[0], hutter[1]/1000, yerr=hutter[2]/1000, marker='o', mfc='k', fmt='o', ecolor='k', label='Exp')
    
    plt.errorbar([t*cv/hfg for t in hutter[0]], [rho_l*g*(d/1000)*(d/1000)/sigma_s for d in hutter[1]], yerr=[rho_l*g*(d/1000)*(d/1000)/(sigma_s) for d in hutter[2]], marker='o', mfc='k', fmt='o', ecolor='k', label='Exp')





       


    # Ejes y leyenda

    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
    
    plt.ylabel('Bo', rotation='horizontal', labelpad=15)

    plt.xlabel('Ja')

    plt.legend(loc = 'best', framealpha=1)





    if args.png == True:

        plt.savefig( 'Bo_vs_Ja.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:
        
        plt.savefig( 'Bo_vs_Ja.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )

          

    plt.gcf().clear()

    # plt.ioff()
