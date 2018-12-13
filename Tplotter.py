
import os
import sys
import argparse
from classy import Class
import numpy as np
import matplotlib.pyplot as plt

def myparser():
    parser=argparse.ArgumentParser(
        description='A script to plot thermal evolution'
    )

    parser.add_argument('-A','--A_bidm', dest='A_bidm', nargs='+', type=float,
                        default=[], help='Specify the coupling stregth A_bidm')
    parser.add_argument('-a','--a_bidm', dest='a_bidm', nargs='+', type=float,
                        default=[], help='Specify the temperature ratio a_bidm')
    parser.add_argument('-M','--M_bidm', dest='M_bidm', nargs='+', type=float,
                        default=[], help='Specify the dark matter mass')
    parser.add_argument('-D','--Delta_bidm', dest='Delta_bidm', nargs='+', type=float,
                        default=[], help='Specify the resonance mass')
    parser.add_argument('-e','--epsilon', dest='epsilon', nargs='+', type=float,
                        default=[], help='Specify resonance energy difference')
    parser.add_argument('-f','--f_bidm', dest='f_bidm', nargs='+', type=float,
                        default=[], help='Specify the interacting dark matter ratio')
    parser.add_argument('-zr','--z_reiomod_start', dest='z_reiomod_start', nargs='+', type=float,
                        default=[], help='Specify when reionization module starts')
    parser.add_argument('-n','--n_bidm', dest='n_bidm', nargs='+', type=float,
                        default=[], help='Specify the dark matter power law index')
    parser.add_argument('-t','--bidm_type', type=str, dest='bidm_type', default='resonance',
                        choices=['resonance','powerlaw'],
                        help='Specify the type of bidm')
    parser.add_argument(
        '-p, --print',
        dest='printfile', default='plot.pdf',
        help=('print the graph directly in a file.'))
    return parser



def main():
    parser=myparser()
    args = parser.parse_args()
    #s = 'A = ' + repr(args.A_bidm)
    cosmo=Class()
    cosmo0=Class()
    title = 'Input:\n'
    cosmo.set({'gauge':'newtonian','output':'tCl mPk dTk vTk','omega_cdm':0.12038,'z_reio':11.357,'reionization_z_start_max':750})
    cosmo0.set({'a_bidm':0.01,'f_bidm':0.4,'A_bidm':0,'gauge':'newtonian','output':'tCl mPk dTk vTk','omega_cdm':0.12038,'z_reio':11.357,'reionization_z_start_max':750})
    #print(s)
    if args.A_bidm:
        cosmo.set({'A_bidm':args.A_bidm[0]})
        title += 'A_bidm = ' + repr(args.A_bidm[0]) + '\n'
    if args.a_bidm:
        cosmo.set({'a_bidm':args.a_bidm[0]})
        title += 'a_bidm = ' + repr(args.a_bidm[0]) + '\n'
    if args.M_bidm:
        cosmo.set({'m_bidm':args.M_bidm[0]})
        title += 'm_bidm = ' + repr(args.M_bidm[0]) + '\n'
    if args.Delta_bidm:
        cosmo.set({'Delta_bidm':args.Delta_bidm[0]})
        title += 'Delta_bidm = ' + repr(args.Delta_bidm[0]) + '\n'
    if args.epsilon:
        cosmo.set({'epsilon_bidm':args.epsilon[0]})
        title += 'epsilon = ' + repr(args.epsilon[0]) + '\n'
    if args.f_bidm:
        cosmo.set({'f_bidm':args.f_bidm[0]})
        title += 'f_bidm = ' + repr(args.f_bidm[0]) + '\n'
    if args.bidm_type:
        cosmo.set({'bidm_type':args.bidm_type})
        title += 'bidm_type = ' + repr(args.bidm_type) + '\n'
    if args.n_bidm:
        cosmo.set({'n_bidm':args.n_bidm[0]})
        title += 'n_bidm = ' + repr(args.n_bidm[0]) + '\n'
    if args.z_reiomod_start:
        cosmo.set({'z_reiomod_start':args.z_reiomod_start[0]})
        cosmo0.set({'z_reiomod_start':args.z_reiomod_start[0]})
        title += 'z_reiomod_start = ' + repr(args.z_reiomod_start[0]) + '\n'
    else:
        cosmo.set({'z_reiomod_start':30})
        cosmo0.set({'z_reiomod_start':30})
        title += 'z_reiomod_start = 30\n'

    cosmo.compute()
    cosmo0.compute()
    thermo = cosmo.get_thermodynamics()
    thermo0 = cosmo0.get_thermodynamics()
    tau = thermo['conf. time [Mpc]']
    Tb = thermo['Tb [K]']
    Tb0 = thermo0['Tb [K]']
    Tdm = thermo['Tbidm [K]']
    Tdm0 = thermo0['Tbidm [K]']
    R = thermo['Rbidm']
    sigma=thermo['sigma_b_dm']

    fig, axes = plt.subplots(nrows=4,ncols=2)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    fig.set_size_inches(10,16)
    fig.suptitle(title)

    axes[0,0].semilogy(tau,Tb)
    axes[0,0].set_title('Baryon temperature')
    axes[0,0].set_xlabel('conf. time [Mpc]')
    axes[0,0].set_ylabel('Tb [K]')

    axes[0,1].semilogy(tau,Tdm)
    axes[0,1].set_title('DM temperature')
    axes[0,1].set_xlabel('conf. time [Mpc]')
    axes[0,1].set_ylabel('Tdm [K]')

    axes[1,0].plot(tau,Tb-Tb0)
    axes[1,0].set_title('Baryon temperature difference')
    axes[1,0].set_xlabel('conf. time [Mpc]')
    axes[1,0].set_ylabel('$\Delta$Tb [K]')

    axes[1,1].plot(tau,Tdm-Tdm0)
    axes[1,1].set_title('DM temperature difference')
    axes[1,1].set_xlabel('conf. time [Mpc]')
    axes[1,1].set_ylabel('$\Delta$Tdm [K]')

    axes[2,0].plot(tau,Tb/Tb0)
    axes[2,0].set_title('Baryon temperature ratio')
    axes[2,0].set_xlabel('conf. time [Mpc]')
    axes[2,0].set_ylabel('Tb ratio')

    axes[2,1].plot(tau,Tdm/Tdm0)
    axes[2,1].set_title('DM temperature ratio')
    axes[2,1].set_xlabel('conf. time [Mpc]')
    axes[2,1].set_ylabel('Tdm ratio')

    axes[3,0].semilogy(tau,R)
    axes[3,0].set_title('coupling strength')
    axes[3,0].set_xlabel('conf. time [Mpc]')
    axes[3,0].set_ylabel('R')

    axes[3,1].semilogy(tau,sigma)
    axes[3,1].set_title('Cross section')
    axes[3,1].set_xlabel('conf. time [Mpc]')
    axes[3,1].set_ylabel('sigma')


    fig.savefig(args.printfile)



main()
