# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 12:18:33 2023

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
from generator import Gener

ge = Gener(alpha_d=0.79, k_B=1.11, k_omega=0.92, A=350, B_delta=.6, k_e=1.21)
print(f'{ge.arnold = :.0f}')

ge.frequency(power=100, u_max=210, k_ld=1.75)
print(f'{ge.power_set = :.0f}')
print(f'{ge.n = :.0f}')

# pi = np.linspace(5, 100, 50)
# n1 = np.zeros(50)
# n2 = np.zeros(50)
# n3 = np.zeros(50)
# n4 = np.zeros(50)

# for i in range(50):
#     n1[i] = ge.frequency(power=pi[i], u_max=120, k_ld=1.8)/1000
#     n2[i] = ge.frequency(power=pi[i], u_max=150, k_ld=1.8)/1000
#     n3[i] = ge.frequency(power=pi[i], u_max=180, k_ld=1.8)/1000
#     n4[i] = ge.frequency(power=pi[i], u_max=210, k_ld=1.8)/1000
    
# plt.plot(pi, n1, label='$u_{max}=120$')
# plt.plot(pi, n2, label='$u_{max}=150$')
# plt.plot(pi, n3, label='$u_{max}=180$')
# plt.plot(pi, n4, label='$u_{max}=210$')

# plt.ylabel('Частота вращения, об/мин *1000') 
# plt.xlabel('Мощность, кВА') 
# plt.grid(linestyle='--', linewidth=0.5, color='black') # сетка
# plt.legend()
# plt.show()


