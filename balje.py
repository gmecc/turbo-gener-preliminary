# -*- coding: utf-8 -*-
"""
Created on Wed May 17 11:51:51 2023

@author: User
"""

import numpy as np
import matplotlib.pyplot as plt 

class Balje:
    def __init__(self):
        pass
    
    def plot(self, max_point=False):
        ng = 200
        Ns = np.linspace(0.02, 1.2, ng)
        nu = np.zeros(ng)
        v = np.zeros(ng)
        
        v = 0.737 * Ns**0.2
        nu = 0.87 - 1.07 * (Ns-0.55)**2 - 0.5 * (Ns-0.55)**3
        Ns_max = Ns[nu.argmax()]
        v_opt = v[nu.argmax()]
        
        print('Максимум КПД', "%.3f"% nu.max())
        print('К-т быстроходности', "%.3f"% Ns_max)
        print('К-т скорости', "%.3f"% v_opt)
        
        if max_point == True:
            plt.vlines(Ns[nu.argmax()], 0.3, 0.9, linewidth=0.5, linestyle='--', color='black')
            plt.scatter(Ns_max, nu.max(), color='red')
            
        plt.plot(Ns, nu, c='red', label='efc')
        plt.plot(Ns, v, c='blue', label='u/Co')
        plt.xlabel('Коэффициент быстроходности', fontsize= 10) 
        plt.ylabel('Параметры', fontsize= 10) 
        plt.legend()
        plt.grid(linestyle='--', linewidth=0.5)
        plt.minorticks_on()
        plt.savefig('balje.png', dpi = 1000)
        # plt.title(self.name, fontsize= 10 , loc='left')
        plt.show()


# pre = Balje()
# pre.plot()
