# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:48:29 2023
Программа предварительного расчета турбинной ступени
Оптимизация по КПД
Создание экземпляра класса - tu = turbo('air', T_in=950, P_in=3.5, P_out=1)
Расчет при оптимальной частоте вращения - power(self, pwr)
Расчет при заданной частоте вращения - powernset(self, pwr, ns)
Построение графика PWR=f(n_opt) - powerplot(self)
@author: User
"""

import pandas as pd
import numpy as np
from scipy import constants as cst
import math
import matplotlib.pyplot as plt 

prop = pd.DataFrame({
    'mol': [28.965, 16.043, 0, 0],
    'k': [1.4017, 1.3053, 0, 0]},
    index=['air', 'methane', 'nitrogen', 'helium'],
    dtype=float)

class TurboGenOptim:
    def __init__(self, pit, T_in, fluid='air', P_out=cst.atm):
        self.fluid = fluid
        self.T_in = T_in
        self.pit = pit
        self.P_out = P_out 
        self.R = cst.R / prop.mol[self.fluid]*1000 # удельная газовая постоянная (Дж/кг*К)
        self.k = prop.k[self.fluid] # показатель адиабаты
        self.Cp = self.k / (self.k - 1) * self.R # удельная изобарная теплоемкость (Дж/кг*К)
        self.h0 = self.Cp * self.T_in
        self.dh1s = self.Cp * self.T_in * (1 - 1 / (self.pit**((self.k-1)/self.k))) 
        
    def rotation_frequency_opt(self, pwr):
        self.efc = .87
        self.dh1 = self.dh1s * self.efc
        self.T_out = (self.h0 - self.dh1)/ self.Cp
        self.G = pwr / self.dh1 
        self.V2 = self.R * self.T_out / self.P_out 
        self.Gv = self.G * self.V2 
        self.n_opt = 0.548 * (self.dh1s)**(3/4) / ( 2 * math.pi * (self.Gv**0.5))
        return self.n_opt
    
    def arnold(self, n, pwr, u_max, k_ld=1.8):
        self.alpha_d = 0.64
        self.k_f = 1.11
        self.k_0 = 0.92
        self.A = 3e4
        self.B_delta = 0.45
        self.k_e = 1.2
        self.u_max = u_max
        self.d_rot = u_max / (math.pi * n)
        self.k_ld = k_ld
        self.l = self.d_rot * self.k_ld
        self.CA_param = 2 / (math.pi * self.alpha_d * self.k_f * self.k_0 * self.A * self.B_delta)
        self.CA = self.d_rot**2 * self.l * n / (self.k_e * pwr)
        self.k_arnold = self.CA / self.CA_param
        return self.CA      
    
    def turbogenerator(self, pwr, efc_gen=.95): # расчет постоянной Арнольда
        self.pwr = pwr 
        pwr_turbine = pwr / efc_gen
        koeff_pow = .98
        self.rotation_frequency_opt(pwr_turbine)
        print(f'Частота вращения оптимальная {self.n_opt*60:.0f}')
        self.arnold(n=self.n_opt, pwr=pwr, u_max=250) 
        print(f'Постоянная Арнольда {self.CA:.3e}')
        print(f'Коэффициент постоянной Арнольда {self.k_arnold:.3f}')

    def powergen(self, n):
        d_rot = self.u_max / (math.pi * n)
        l = d_rot * self.k_ld
        Pn = d_rot ** 2 * l * n / (self.k_e * self.CA)
        return Pn

    def plot(self, pwr):
        pwr_min, pwr_max = pwr
        pwri = np.linspace(pwr_min, pwr_max)
        n_opt = self.rotation_frequency_opt(pwri)
        plt.plot(n_opt/1000*60, pwri/1000, c='red', label='turbine')
        
        Pn = self.powergen(n=n_opt)
        plt.plot(n_opt*60/1000, Pn/1000, c='blue', label='generator')
        
        plt.hlines(self.pwr/1000, n_opt[0]/1000*60, n_opt[-1]/1000*60, linewidth=0.5, linestyle='--', color='black')
        
        plt.xlabel('Частота вращения, т.об/мин', fontsize= 10) 
        plt.ylabel('Мощность, кВт', fontsize= 10) 
        plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.savefig('turbine-optim.png', dpi = 300)
        plt.show()


tu = TurboGenOptim(pit=3, T_in=1250) # создание экземпляра класса turbo
tu.turbogenerator(pwr=1e5)
tu.plot(pwr=(20000, 200000))





