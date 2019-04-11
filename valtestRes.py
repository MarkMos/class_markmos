import numpy as np
from classy import Class

M = {1, 100, 1000, 5000, 10000}
A = {5e-5,1e-4,5e-4}
a = {1e-6,1e-5,1e-4,1e-3,1e-2}
f = {0.5,0.99}
eps = {1e-9,1e-10,1e-11,5e-12}

cosmo = Class()

ndone = 0
ntodo = len(M)*len(A)*len(a)*len(f)*len(eps)

for m in M:
    for As in A:
        for aa in a:
            for fs in f:
                for e in eps:
                    cosmo.set({'gauge':'synchronous',
                               'output':'tCl, lCl, mPk, pCl',
                               'omega_cdm':0.12038,
                               'recombination':'recfast',
                               'h':0.67556,
                               'lensing':'yes',
                               'tight_coupling_trigger_tau_c_over_tau_h':0.002,
                               'tight_coupling_trigger_tau_c_over_tau_k':0.0003,
                               'f_bidm':fs,
                               'm_bidm':m,
                               'bidm_type':'resonance',
                               'a_bidm':aa,
                               'A_bidm':As,
                               'epsilon_bidm':e
                               })
                    print('Beginning: M='+str(m)
                          + ' A=' + str(As)
                          + ' a=' + str(aa)
                          + ' f=' + str(fs)
                          + ' eps=' + str(e)
                         )
                    cosmo.compute()
                    ndone+=1
                    print('Done, ' + str(ndone) + ' of ' + str(ntodo))
                    cosmo.struct_cleanup()
