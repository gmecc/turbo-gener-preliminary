# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 20:48:29 2023
Программа расчета главных размеров генератора
Частота вращения - [1/c]
@author: User
"""

import numpy as np
import math
from scipy.optimize import root
import matplotlib.pyplot as plt

class Gener:
    def __init__(self, alpha_d=0.64, k_B=1.11, k_omega=0.92, A=200, B_delta=.45, k_e=1.21):
        self.alpha_d = alpha_d # расчетный коэффициент полюсного перекрытия
        self.k_B = k_B # коэффициент формы поля
        self.k_omega = k_omega # обмоточный коэффициент
        self.A = A # линейная нагрузка [A/см]
        self.B_delta = B_delta # индукция в зазоре [Тл]
        self.k_e = k_e # коэффициент учитывающий внутреннее падение напряжения в генераторе
        
        self.arnold = 6.1e7 / (self.alpha_d * self.k_B * self.k_omega * self.A * self.B_delta)
       
    def powergen(self, n, u_max=120, k_ld=1.5, delta=1):
        self.u_max = u_max # допустимая окружная скорость по диаметру ротора
        self.k_ld = k_ld # соотношение длины статора к диаметру расточки L/D
        self.n = n # Номинальная частота вращения, об/мин
        self.delta = delta # Зазор между статором и ротором, мм
        
        self.d_rot = self.u_max / (math.pi * self.n / 60) # диаметр ротора [м]
        self.d_stat = self.d_rot + self.delta * .002 # диаметр расточки статора [м]
        self.l = self.d_stat * self.k_ld # расчетная длина статора [м]
        self.power = self.d_stat ** 2 * self.l * n / (self.k_e * self.arnold) * 1e9 # мощность генератора [ВА] 
        return self.power         
    
    def func(self, n):
        residual = np.abs(self.powergen(n=n, u_max=self.u_max, k_ld=self.k_ld, delta=self.delta) - 
                          self.power_set)
        return residual
        
    def frequency(self, power, u_max=120, k_ld=1.5, delta=1):
        # нахождение частоты вращения ротора по известной мощности
        # методом решения обратной задачи
        
        self.u_max = u_max # допустимая окружная скорость по диаметру ротора
        self.k_ld = k_ld # соотношение длины статора к диаметру расточки L/D
        self.delta = delta # Зазор между статором и ротором, мм
        self.power_set = power * 1000
        
        self.sol = root(self.func, 1000)
        self.n = self.sol.x[0] # Номинальная частота вращения, об/мин
        
        return self.n

    



# n = 12000

# ge = gener()
# print(f'{ge.arnold = :.0f}')

# ge.powergen(n=n)
# print(f'{ge.d_rot = :.4f}')
# print(f'{ge.d_stat = :.4f}')
# print(f'{ge.l = :.4f}')
# print(f'{ge.power = :.0f}')

# ge.frequency(power=103.102)
# print(f'{ge.power_set = :.0f}')
# print(f'{ge.n = :.0f}')





# n = np.linspace(200, 1000, 50)
# plt.plot(n*60/1000, Pn/1000, color='red')


# print(n)
# print(ge.powergen_fn(n=n, u_max=200, k_ld=2))

    # def povergen(self, u_max, k_ld):
    #     self.k_ld = k_ld
    #     self.u_max = u_max
    #     d_rot = np.linspace(self.d_min, self.d_max, 50)
    #     n = u_max / (math.pi * d_rot) 
    #     l = d_rot * k_ld
    #     Pn = 2 * math.pi * d_rot ** 2 * l * n / (self.k_e * self.CA)
    #     return n, Pn 


