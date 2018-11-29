
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
    parser.add_argument('-f','--f_bidm', dest='f_bidm', nargs='+', type=float,
                        default=[], help='Specify the interacting dark matter ratio')
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
    cosmo.set({'gauge':'newtonian','output':'tCl mPk dTk vTk','omega_cdm':0.12038})
    cosmo0.set({'a_bidm':0.01,'f_bidm':0.4,'A_bidm':0,'gauge':'newtonian','output':'tCl mPk dTk vTk','omega_cdm':0.12038})
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
    if args.f_bidm:
        cosmo.set({'f_bidm':args.f_bidm[0]})
        title += 'f_bidm = ' + repr(args.f_bidm[0]) + '\n'

    cosmo.compute()
    cosmo0.compute()
    thermo = cosmo.get_thermodynamics()
    thermo0 = cosmo0.get_thermodynamics()
    tau = thermo['conf. time [Mpc]']
    Tb = thermo['Tb [K]']
    Tb0 = thermo0['Tb [K]']
    Tdm = thermo['Tbidm [K]']
    Tdm0 = thermo0['Tbidm [K]']

    fig, axes = plt.subplots(nrows=3,ncols=2)
    fig.subplots_adjust(hspace=0.4, wspace=0.4)
    fig.set_size_inches(10,12)
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

    fig.savefig(args.printfile)



main()
