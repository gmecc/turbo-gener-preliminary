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

df = pd.DataFrame({
    'mol': [28.965, 16.043, 0, 0],
    'k': [1.4017, 1.3053, 0, 0]},
    index=['air', 'methane', 'nitrogen', 'helium'],
    dtype=float)

ds = pd.Series(index=[
    'R', 
    'k', 
    'Cp',
    'T_in',
    'P_in',
    'P_out',
    'pit',
    'h0',
    'dh1s', 
    'n_opt',
    'efc',
    'pwr',
    'n',
    'dh1',
    'T_out',
    'G',
    'V2',
    'Gv',
    'mfp',
    'Ns',
    'efcp',
    'efcs',
    'n_optm',
    ], dtype=float)

pd.set_option('display.float_format', '{:.4f}'.format)

class turbo:
    def __init__(self, name, T_in, P_in, P_out):
        self.name = name
        self.T_in = T_in
        self.P_in = P_in
        self.P_out = P_out        
        self.R = cst.R / df.mol[self.name] # удельная газовая постоянная (кДж/кг*К)
        self.k = df.k[self.name] # показатель адиабаты
        self.Cp = self.k / (self.k - 1) * self.R # удельная изобарная теплоемкость (кДж/кг*К)
        self.pit = P_in / P_out
        self.h0 = self.Cp * self.T_in
        self.dh1s = self.Cp * self.T_in * (1 - 1 / (self.pit**((self.k-1)/self.k))) 
        ds.R = self.R
        ds.k = self.k
        ds.Cp = self.Cp
        ds.P_in = self.P_in
        ds.P_out = self.P_out
        ds.pit = self.pit
        ds.h0 = self.h0
        ds.dh1s = self.dh1s
        ds.T_in = self.T_in

    def _solve(self, efc, pwr, n):
        self.efc = efc
        # self.pwr = pwr
        self.n = n
        self.dh1 = self.dh1s * efc
        self.T_out = (self.h0 - self.dh1s)/ self.Cp
        self.G = self.pwr / self.dh1 
        self.V2 = self.R * self.T_out / self.P_out / 100
        self.Gv = self.G * self.V2 
        self.mfp = self.G * self.T_in**0.5 / self.P_in * 10
        self.Ns = 2 * math.pi * n * (self.Gv**0.5) / (self.dh1*1000)**(3/4) 
        self.n_opt = 0.5 * (self.dh1*1000)**(3/4) / (2 * math.pi * (self.Gv**0.5))
        # self.n_opt = self.n_opts * 60 
        self.efcs = 0.87 - 1.07 * (self.Ns-0.55)**2 - 0.5 * (self.Ns-0.55)**3
        ds.efc = self.efc
        ds.pwr = self.pwr
        ds.n = self.n * 60
        ds.dh1 = self.dh1
        ds.T_out = self.T_out
        ds.G = self.G
        ds.V2 = self.V2
        ds.Gv = self.Gv
        ds.mfp = self.mfp
        ds.Ns = self.Ns
        ds.efcs = self.efcs
        ds.n_opt = self.n_opt       

    def power(self, pwr): # оптимизация при n_opt
        self.pwr = pwr
        self.n = 100
        self._solve(efc=0.8, pwr=self.pwr, n=self.n)
        self.ef = 0.6
        while abs(self.ef - self.efcs) > 0.002:
            self.ef += 0.001
            self._solve(efc=self.ef, pwr=self.pwr, n=self.n_opt)
        ds.n_optm = self.n_opt * 60  
        ds.efcp = self.efcs
        return self.n_opt * 60

    def powernset(self, pwr, ns): # оптимизация при заданной n
        self.pwr = pwr
        self.ns = ns
        self.n = 100
        self._solve(efc=0.8, pwr=self.pwr, n=self.n)
        self.ef = 0.6
        while abs(self.ef - self.efcs) > 0.002:
            self.ef += 0.001
            self._solve(efc=self.ef, pwr=self.pwr, n=self.ns)
    
    def powerplot(self):
        ng = 50
        nsi = np.zeros(ng)
        pwri = np.linspace(10, 200, ng)
        for i in range(ng):
            self.power(pwri[i])
            nsi[i] = self.n_opt * 60 / 1000
        
        # ПОСТРОЕНИЕ ГРАФИКА
        plt.plot(nsi, pwri, c='red', label='turbine')
        plt.xlabel('Частота вращения, т.об/мин', fontsize= 10) 
        plt.ylabel('Мощность, кВт', fontsize= 10) 
        # plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.title(self.name, fontsize= 10 , loc='left')
        # plt.show()

class gener:
    def __init__(self):
        alpha_d = 0.64
        k_f = 1.11
        k_0 = 0.92
        A = 3e4
        B_delta = 0.45
        self.k_e = 1.2
        self.CA = 2 / (math.pi * alpha_d * k_f * k_0 * A * B_delta)
    def povergen(self, u_max, k_ld):
        self.k_ld = k_ld
        self.u_max = u_max
        d_rot = np.arange(0.04, 0.18, 0.01)
        n = u_max / (math.pi * d_rot) 
        l = d_rot * k_ld
        Pn = 2 * math.pi * d_rot ** 2 * l * n / (self.k_e * self.CA)
        return n, Pn, d_rot        



tu = turbo('air', T_in=300, P_in=12, P_out=6) # создание экземпляра класса turbo
tu.powerplot()




# tu = turbo('air', T_in=300, P_in=3.5, P_out=1) # создание экземпляра класса turbo
# tu.power(pwr=50) # оптимизация при n_opt
# tu.powernset(pwr=50, ns=900) # оптимизация при заданной n
# # print(ds)
# print('Мощность pwr', "%.1f"% ds.pwr)
# print('Оптимальная частота вращения n_optm', "%.0f"% ds.n_optm)
# print('КПД оптимальный efcp', "%.3f"% ds.efcp)
# print('Заданная частота вращения n', "%.0f"% ds.n)
# print('Расчетный КПД efcs', "%.3f"% ds.efcs)

# ge = gener()
# n, Pn, d_rot = ge.povergen(u_max=210, k_ld=1.75)
# plt.xlabel('n, krpm') 
# plt.ylabel('Pn, kW') 
# plt.plot(n*60/1000, Pn/1000, label='generator')
# plt.legend()
# # plt.grid()
# plt.show()


