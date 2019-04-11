import numpy as np
from classy import Class

M = {0.1, 1, 100, 1000, 5000, 10000}
A = {1e-42,5e-42,1e-41,5e-41,1e-40,5e-40,1e-39}
a = {1e-6,1e-5,1e-4,1e-3,1e-2,1e-1,1}
f = {0.01,0.1,0.5,0.99}

cosmo = Class()

ndone = 0
ntodo = len(M)*len(A)*len(a)*len(f)

for m in M:
    for As in A:
        for aa in a:
            for fs in f:
                cosmo.set({'gauge':'synchronous',
                           'output':'tCl, lCl, mPk, pCl',
                           'omega_cdm':0.12038,
                           'recombination':'recfast',
                           'h':0.67556,
                           'lensing':'yes',
                           'tight_coupling_trigger_tau_c_over_tau_h':0.008,
                           'tight_coupling_trigger_tau_c_over_tau_k':0.001,
                           'f_bidm':fs,
                           'm_bidm':m,
                           'bidm_type':'powerlaw',
                           'n_bidm':-4,
                           'a_bidm':aa,
                           'A_bidm':As
                           })
                print('Beginning: M='+str(m)
                      + ' A=' + str(As)
                      + ' a=' + str(aa)
                      + ' f=' + str(fs)
                     )
                cosmo.compute()
                ndone+=1
                print('Done, ' + str(ndone) + ' of ' + str(ntodo))
                cosmo.struct_cleanup()
