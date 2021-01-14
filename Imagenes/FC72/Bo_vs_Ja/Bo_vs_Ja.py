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

    rho_l_exp = 1620.

    g_exp = 9.81

    sigma_s_exp = 0.00827

    cv_exp = 1098.

    hfg_exp = 84500.  


    Ja_exp = [ t*cv_exp/hfg_exp for t in hutter[0] ]

    Bo_exp = [ (rho_l_exp*g_exp/sigma_s_exp)*((d/1000)**2) for d in hutter[1] ]

    Bo_exp_err = [ 2*(rho_l_exp*g_exp/sigma_s_exp)*(d/1000)*(e/1000) for d,e in zip(hutter[1],hutter[2]) ]

    
    # plt.errorbar(hutter[0], hutter[1], yerr=hutter[2], marker='o', mfc='k', fmt='o', ecolor='k', label='Experimento')
    plt.errorbar(Ja_exp, Bo_exp, yerr=Bo_exp_err, marker='o', mfc='k', fmt='o', ecolor='k', label='Experimento')





    # Simulaciones

    lb = np.loadtxt('D_vs_supheat_LB.dat', unpack=True)

    rho_l_lb = 7.949

    sigma_s_lb = 0.26874*2.

    cv_lb = 11.

    hfg_lb = 0.315574

    Ts_lb = 0.0262


    Ja_lb = [ (t-Ts_lb)*cv_lb/hfg_lb for t in lb[0] ]

    Bo_lb = [ (rho_l_lb*g/sigma_s_lb)*(d**2) for d,g in zip(lb[1],lb[2]) ]
    
    # plt.plot(Ja_lb, Bo_lb, marker='s', mfc='r', mec='r', linestyle='None', label='LB')
    plt.errorbar(Ja_lb, Bo_lb, marker='s', mfc='r', mec='r', fmt='s', ecolor='r', label='LB')



       


    # Ejes y leyenda

    locale.setlocale(locale.LC_ALL, "es_AR.UTF-8")
    
    plt.ylabel('Bo', rotation='horizontal', labelpad=15)

    plt.xlabel('Ja')

    plt.legend(loc = 'upper left', framealpha=1)





    if args.png == True:

        plt.savefig( 'Bo_vs_Ja.png', format='png', bbox_inches = 'tight', dpi=600 )

    else:
        
        plt.savefig( 'Bo_vs_Ja.pdf', format='pdf', bbox_inches = 'tight', dpi=600 )

          

    plt.gcf().clear()

    # plt.ioff()
