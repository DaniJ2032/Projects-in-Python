import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

PRBSI             = np.array ([1,1,0,1,0,1,0,1,0])
berI              = np.zeros(1024)
salidaPRBSI       = []
PRBSI_AUX         = []
Nsymb             = 511
acumulador        = 0
acumulador_arreglo = []
firreg = np.zeros(5)
latencia = 3
latencia_minima = 0

for j in range(511*3):

    for i in range(Nsymb):
        berI = np.roll(berI,1)
        firreg = np.roll(firreg,1)
        PRBSI    = np.roll(PRBSI,1)
        PRBSI[0] = PRBSI[0] ^ PRBSI[5]
        PRBSI_AUX.append(PRBSI[8])
        if PRBSI[8] == 0:
            berI[0]   = 0
            firreg[0] = 0
        else:
            berI[0]   = 1
            firreg[0] = 1
    
        
        acumulador = acumulador + (int(berI[j]) ^ int(firreg[latencia])) 


    acumulador_arreglo.append(acumulador)
    if (acumulador <= latencia_minima):
        latencia_minima = acumulador
        print(j)
    acumulador = 0    


print(acumulador)
print(acumulador_arreglo)