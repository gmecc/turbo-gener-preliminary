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

class turbo:
    def __init__(self, name, T_in, P_out):
        self.name = name
        self.T_in = T_in
        self.P_out = P_out        
        self.R = cst.R / df.mol[self.name] # удельная газовая постоянная (кДж/кг*К)
        self.k = df.k[self.name] # показатель адиабаты
        self.Cp = self.k / (self.k - 1) * self.R # удельная изобарная теплоемкость (кДж/кг*К)
        self.h0 = self.Cp * self.T_in # энтальпия на входе

    def optim(self, efc, pwr, pit):
        self.efc = efc
        self.pwr = pwr
        self.pit = pit # степень понижения давления в турбине
        self.dh02s = self.Cp * self.T_in * (1 - 1 / (self.pit**((self.k-1)/self.k))) # изоэнтропный перепад энтальпий в турбине 
        self.dh02 = self.dh02s * efc # фактический перепад энтальпий в турбине
        self.T_out = self.T_in - self.dh02 / self.Cp # температура на выходе из турбины
        self.G = self.pwr / self.dh02 # массовый расход рабочего тела
        self.V2 = self.R * self.T_out / self.P_out / 100 # удельный объем рабочего тела на выходе из турбины
        self.Gv = self.G * self.V2 # объемный расход рабочего тела на выходе из турбины
        self.n_opt = 0.548 * (self.dh02s*1000)**(3/4) / (2 * math.pi * (self.Gv**0.5))
        self.n_opt = self.n_opt * 60 /1000
        return self.n_opt
    
    def optim_plot(self, p, pit):
        ng = 50
        p_min, p_max = p
        pwri = np.linspace(p_min, p_max, ng)
        
        for i in range(len(pit)):
            nsi = self.optim(efc=0.867, pwr=pwri, pit=pit[i])
            plt.plot(nsi, pwri, label=f'Пt={pit[i]}')
        
        plt.xlabel('Оптимальная частота вращения, т.об/мин', fontsize= 10) 
        plt.ylabel('Мощность, кВт', fontsize= 10) 
        plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.savefig('turbo-optim.jpg', dpi = 300)
        plt.minorticks_on()
        # plt.title(self.name, fontsize= 10 , loc='left')
        plt.show()


# tu = turbo('methane', T_in=300, P_out=6) # создание экземпляра класса turbo
# tu.optim_plot(p=(20, 250), pit=(2, 2.5, 3))




