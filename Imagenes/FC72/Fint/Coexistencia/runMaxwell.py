import os
import MaxwellConstruction as mx
import numpy as np
import matplotlib.pyplot as plt
import argparse


def run_pr_case( a_eos, b_eos, w_eos, sigma, beta, TrList ):
    
    """
    Ejecucion de casos de construccion de Maxwell
    """   

    
    # Directorio del caso y limpieza

    main_dir = os.getcwd()

    cases_dir = main_dir + '/a_{:.4f}_b_{:.4f}_w_{:.4f}_sigma_{:.4f}_beta_{:.4f}/'.format(a_eos, b_eos, w_eos, sigma, beta)

    os.system('rm -rf ' + cases_dir )

    os.system('mkdir -p ' + cases_dir )



    # Ecuacion de estado

    prob = mx.EOS('Peng-Robinson',a=a_eos,b=b_eos,w=w_eos)



    # Ejecucion para cada T reducida
    
    for Tr in TrList:

        

        # Directorio de ejecucion

        os.chdir( cases_dir )       
        
        case_name = 'Tr_{:.3f}'.format(Tr)

        os.system('cp -r ../Base ' + case_name )

        os.chdir( cases_dir + '/' + case_name)



        # Propiedades de coexistencia

        step = 0.999
        if Tr < 0.6:
            step = 0.9999
        
    
        if Tr >= 0.8:
            Vrmin,Vrmax = mx.coexistencia(prob, Tr, plotPV=False, Vspace=(0.3,50,10000), step_size=step)

        else:
            Vrmin,Vrmax = mx.coexistencia(prob, Tr, plotPV=False, Vspace=(0.28,4000,200000), step_size=step)          

        
           
        # Reemplazo de propiedades
        
        os.system('sed -i \'s/sigmaReplace/{:.5g}/g\' Allrun'.format(args.sigma))

        os.system('sed -i \'s/beta_pr_replace/{:.5g}/g\' properties/macroProperties'.format(args.beta))
        
        os.system('sed -i \'s/a_pr_replace/{:.5g}/g\' properties/macroProperties'.format(args.a))

        os.system('sed -i \'s/b_pr_replace/{:.5g}/g\' properties/macroProperties'.format(args.b))

        os.system('sed -i \'s/w_pr_replace/{:.5g}/g\' properties/macroProperties'.format(args.w))

        os.system('sed -i \'s/T_pr_replace/{:.7g}/g\' start/initialFields'.format(Tr*prob.Tc()))

        os.system('sed -i \'s/rhomin_pr_replace/{:.7g}/g\' start/initialFields'.format(prob.rhoc()/Vrmax))

        os.system('sed -i \'s/rhomax_pr_replace/{:.7g}/g\' start/initialFields'.format(prob.rhoc()/Vrmin))        


    
        # Ejecucion

        print('Tr = {}'.format(Tr))

        os.system('./Allclean > log.Allclean')

        os.system('./Allpre > log.Allpre')

        os.system('./Allrun > log.lbm')

        
    
    os.chdir(main_dir)    

    pass







if __name__ == "__main__":



    # Argumentos de consola
    
    parser = argparse.ArgumentParser(description='Resolución del problema de construcción de Maxwell para diferentes constantes')

    parser.add_argument('-a', help='Constante a de PR', type=float, default = 1./50.)

    parser.add_argument('-b', help='Constante b de PR', type=float, default = 2./21.)

    parser.add_argument('-w', help='Constante w de PR', type=float, default = 0.5)

    parser.add_argument('-beta', help='Constante beta de fuerza de interaccion mixta', type=float, default = 1.25)        

    parser.add_argument('-sigma', help='Constante sigma', type=float, default = 0.125)    

    args = parser.parse_args()


    # Ejecucion de casos

    Tr = [0.95, 0.90, 0.85, 0.80, 0.75, 0.70, 0.65]

    run_pr_case( args.a, args.b, args.w, args.sigma, args.beta, Tr )



    
