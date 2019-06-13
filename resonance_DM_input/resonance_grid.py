import numpy as np
import scipy
from classy import Class
from scipy.interpolate import interp1d

Avals = np.logspace(-12,-5,100)
Mvals = np.logspace(1,4,50)
evals = np.logspace(-11,-6,100)

logAfile= open("logAlist.txt","w+")
for iA in range(0,Avals.size):
    Aval = np.log10(Avals[iA])
    logAfile.write(f'{Aval}\n')
logAfile.close()

logMfile= open("logMlist.txt","w+")
for iM in range(0,Mvals.size):
    Mval = np.log10(Mvals[iM])
    logMfile.write(f'{Mval}\n')
logMfile.close()

logefile= open("logelist.txt","w+")
for ie in range(0,evals.size):
    eval = np.log10(evals[ie])
    logefile.write(f'{eval}\n')
logefile.close()


Ndone = 0
Ntodo = Avals.size*Mvals.size*evals.size

for i in range(0,evals.size):
    epsilon = evals[i]
    models = set()
    moddata = {}
    cosmo = Class()
    for M in Mvals:
        for A in Avals:
            model = 'M=' + str(M) + '-A=' + str(A)
            models.add(model)
            moddata[model]={'Mass':M,'A':A}
            cosmo.set({'gauge':'synchronous',
                                   'omega_cdm':0.12038,
                                   'recombination':'recfast',
                                   'h':0.67556,
                                   'f_bidm':0.99,
                                   'm_bidm':M,
                                   'bidm_type':'resonance',
                                   'a_bidm':1e-8,
                                   'epsilon_bidm':3e-11,
                                   'A_bidm':A,
                                   'tight_coupling_trigger_tau_c_over_tau_h':0.002,
                                   'tight_coupling_trigger_tau_c_over_tau_k':0.0003,
                                   })
            cosmo.compute()
            Th = cosmo.get_thermodynamics()
            Tmax = max(Th['Tbidm [K]'])
            iTmax = np.argmax(Th['Tbidm [K]'])
            zeq = Th['z'][iTmax]
            Ti = interp1d(Th['z'],Th['Tbidm [K]'])
            Tbi = interp1d(Th['z'],Th['Tb [K]'])
            #print(str(A) + ' ' + str(max(Th['z'])))
            Teq = Ti(zeq)
            aeq = Ti(zeq)/Tbi(zeq)
            moddata[model].update({'Teq':Teq,'aeq':aeq,'zeq':zeq})
            cosmo.struct_cleanup()
            Ndone+=1
            print(Ndone/Ntodo)

    AA, MM = np.meshgrid(Avals,Mvals)
    aa = np.zeros(AA.shape)

    for iA in range(0,aa.shape[1]):
        for iM in range(0,aa.shape[0]):
            for m in models:
                if AA[iM,iA] == moddata[m]['A'] and MM[iM,iA] == moddata[m]['Mass']:
                    aa[iM,iA] = moddata[m]['aeq']

    aVals = np.zeros(Avals.size*Mvals.size)

    for iA in range(0,Avals.size):
        for iM in range(0,Mvals.size):
            aVals[iA*Mvals.size+iM]=aa[iM,iA]


    logafile= open(str(i)+"/logagrid.txt","w+")
    for ia in range(0,aVals.size):
        aval = np.log10(aVals[ia])
        logafile.write(f'{aval}\n')
    logafile.close()
