# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:18:33 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
from generator import Gener


n = 12000

ge = Gener()
print(f'{ge.arnold = :.0f}')

ge.powergen(n=n)
print(f'{ge.d_rot = :.4f}')
print(f'{ge.d_stat = :.4f}')
print(f'{ge.l = :.4f}')
print(f'{ge.power = :.0f}')


ni = np.linspace(30000, 120000, 50)
plt.plot(ni/1000, ge.powergen(n=ni, u_max=120, k_ld=1.8)/1000, label='$u_{max}=120$')
plt.plot(ni/1000, ge.powergen(n=ni, u_max=150, k_ld=1.8)/1000, label='$u_{max}=150$')
plt.plot(ni/1000, ge.powergen(n=ni, u_max=180, k_ld=1.8)/1000, label='$u_{max}=180$')
plt.plot(ni/1000, ge.powergen(n=ni, u_max=210, k_ld=1.8)/1000, label='$u_{max}=210$')
plt.xlabel('Частота вращения, об/мин *1000') 
plt.ylabel('Мощность, кВА') 
plt.grid(linestyle='--', linewidth=0.5, color='black') # сетка
plt.legend()
plt.show()

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