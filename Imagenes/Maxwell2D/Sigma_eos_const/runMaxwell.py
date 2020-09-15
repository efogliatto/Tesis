import os
import MaxwellConstruction as mx
import numpy as np
import matplotlib.pyplot as plt
import argparse


def run_vdw_case( a_eos, b_eos, sigma, TrList ):
    
    """
    Ejecucion de casos de construccion de Maxwell
    """   

    
    # Directorio del caso y limpieza

    main_dir = os.getcwd()

    cases_dir = main_dir + '/a_{:.4f}_b_{:.4f}_sigma_{:.4f}/'.format(a_eos, b_eos, sigma)

    os.system('rm -rf ' + cases_dir )

    os.system('mkdir -p ' + cases_dir )



    # Ecuacion de estado

    VdW = mx.EOS('VanDerWaals',a=a_eos,b=b_eos)



    # Ejecucion para cada T reducida
    
    for i,Tr in enumerate(TrList):

        

        # Directorio de ejecucion

        os.chdir( cases_dir )       
        
        case_name = 'Caso{}'.format(i)

        os.system('cp -r ../Base ' + case_name )

        os.chdir( cases_dir + '/' + case_name)


           
        # Reemplazo de propiedades

        step = 0.999
        if Tr < 0.6:
            step = 0.9999

        Vrmin,Vrmax = mx.coexistencia(VdW, Tr, plotPV=False, step_size=step)

        
        os.system('sed -i \'s/sigmaReplace/{:.5g}/g\' properties/macroProperties'.format(args.sigma))
    
        os.system('sed -i \'s/a_vdw_replace/{:.5g}/g\' properties/macroProperties'.format(args.a))

        os.system('sed -i \'s/b_vdw_replace/{:.5g}/g\' properties/macroProperties'.format(args.b))

        os.system('sed -i \'s/T_vdw_replace/{:.7g}/g\' start/initialFields'.format(Tr*VdW.Tc()))

        os.system('sed -i \'s/rho_vdw_replace/{:.7g}/g\' start/initialFields'.format(VdW.rhoc()))


    
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

    parser.add_argument('-a', help='Constante a de vdW', type=float, default = 0.5)

    parser.add_argument('-b', help='Constante b de vdW', type=float, default = 4.0)

    parser.add_argument('-sigma', help='Constante sigma', type=float, default = 0.125)    

    args = parser.parse_args()


    # Ejecucion de casos

    Tr = [0.99, 0.9, 0.8, 0.7, 0.6]

    run_vdw_case( args.a, args.b, args.sigma, Tr )



    
