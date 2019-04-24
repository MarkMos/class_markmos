import numpy as np
import scipy
from classy import Class
from scipy.interpolate import interp1d
from scipy.interpolate import interp2d

Avals = np.logspace(-8,-3,100)
Mvals = np.logspace(1,4,50)


models = set()
moddata = {}
cosmo = Class()

Ndone = 0
Ntodo = Avals.size*Mvals.size

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

for iA in range(0,Avals.size):
    for iM in range(0,Mvals.size):
        aVals[iA*Mvals.size+iM]=aa[iM,iA]

Afile= open("Alist.txt","w+")
for iA in range(0,Avals.size):
    Aval = Avals[iA]
    Afile.write(f'{Aval}\n')
Afile.close()

Mfile= open("Mlist.txt","w+")
for iM in range(0,Mvals.size):
    Mval = Mvals[iM]
    Mfile.write(f'{Mval}\n')
Mfile.close()

afile= open("agrid.txt","w+")
for ia in range(0,aVals.size):
    aval = aVals[ia]
    afile.write(f'{aval}\n')
afile.close()

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

logafile= open("logagrid.txt","w+")
for ia in range(0,aVals.size):
    aval = np.log10(aVals[ia])
    logafile.write(f'{aval}\n')
logafile.close()
