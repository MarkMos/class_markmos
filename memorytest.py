from classy import Class
models = ['idm1','idm2']

cosmo={}
for M in models:
    cosmo[M] = Class()
    cosmo[M].set({'gauge':'newtonian',
                  'output':'tCl',
                  'omega_cdm':0.12038,
                  #'z_reio':11.357,
                  #'reionization_z_start_max':750,
                  #'z_reiomod_start':300,
                  #'recfast_Nz0':80000,
                  #'recfast_z_initial':1e7,
                  'recombination':'recfast',
                  #'recfast_H_frac':3e-4,
                  'reio_parametrization':'reio_none',
                  '100*theta_s':1.042143,
                  'background_verbose':5,
                  'input_verbose':5,
                  #'h':0.47556
                 })
    if M == 'idm1':
        cosmo[M].set({'a_bidm':5e-4,
                      'f_bidm':0.99,
                      'A_bidm':1.7e-41,
                      'm_bidm':1,
                      'n_bidm':-4,
                      'bidm_type':'powerlaw'})
    if M == 'idm2':
        cosmo[M].set({'a_bidm':5e-2,
                      'f_bidm':0.99,
                      'A_bidm':1.9e-41,
                      'm_bidm':100.,
                      'n_bidm':-4,
                      'bidm_type':'powerlaw'})
    print([M])
    for key, val in cosmo[M].pars.items():
        print(key+'='+str(val))
    cosmo[M].compute()
