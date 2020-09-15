import vdWColumn as vdw

import matplotlib.pyplot as plt

import numpy as np

import os


# Solucion con LBM

sigma_0 = np.loadtxt( "sigma_1.25.dat", unpack = True )

sigma_1 = np.loadtxt( "sigma_0.125.dat", unpack = True )

sigma_2 = np.loadtxt( "sigma_0.0125.dat", unpack = True )


plt.style.use('../custom.mplstyle') 

plt.plot( sigma_0[4],
          sigma_0[1],
          label = r'$\sigma=1.25$',
          linestyle = 'None',
          color = 'r',
          marker = 'o',
          mfc = 'None')

plt.plot( sigma_0[5],
          sigma_0[1],
          linestyle = 'None',
          color = 'r',
          marker = 'o',
          mfc = 'None')

plt.plot( sigma_1[4],
          sigma_1[1],
          label = r'$\sigma=0.125$',
          linestyle = 'None',
          color = 'b',
          marker = '^',
          mfc = 'None')

plt.plot( sigma_1[5],
          sigma_1[1],
          linestyle = 'None',
          color = 'b',
          marker = '^',
          mfc = 'None')

plt.plot( sigma_2[4],
          sigma_2[1],
          label = r'$\sigma=0.0125$',
          linestyle = 'None',
          color = 'g',
          marker = 's',
          mfc = 'None')

plt.plot( sigma_2[5],
          sigma_2[1],
          linestyle = 'None',
          color = 'g',
          marker = 's',
          mfc = 'None')






# Solucion analitica

analitica = [ [], [], [] ]

for T in np.linspace(0.5, 0.99, (0.99-0.5)/0.01):
    
    cl, cg = vdw.interphaseDensities(T)

    analitica[0].append(T)

    analitica[1].append(cl)

    analitica[2].append(cg)


    
plt.plot( analitica[1], analitica[0], label = 'VdW')
plt.plot( analitica[2], analitica[0], linestyle = '-')




# Labels

plt.ylabel('$T_r$', rotation='horizontal', labelpad=15)

plt.xlabel(r'$\rho_r$')
# plt.xlabel(r'$c$')

# plt.xlim((-0.4,0.4))

plt.legend(loc='best') 


dirname = os.path.basename( os.getcwd() )

# plt.savefig( 'fig_' + dirname + '.eps', format='eps', dpi=600 )

# plt.savefig( 'fig_' + dirname + '.eps', format='eps', dpi=600 )

plt.savefig( 'fig_' + dirname + '.png', format='png', dpi=600 )

# plt.show()
