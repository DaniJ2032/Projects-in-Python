# |_______________________SinyCosTab_V1.0b_____________________________|
# | Se grafica un periodo completo de un seno y un coseno tomando como |
# | frecuencia de muestreo 100Mhz lo cual la frec maxima a muestrear   |   
# | sera de 50Mhz segun el teorema de Nyquist.                         |      
# | Se busca realizar un muestreo de 1024 valores lo cual dara como    |
# | frecuencia minia a muestrear para 1024 sera:                       |
# | Tsampl = 1/100Mhz --> 10ns                                         |
# | Tmuestras = 10ns * 1024muestras --> 10.24us                        | 
# | Frecmin = 1/10.24us --> 97.65625Khz                                |
# | Aparte se cuantiza los valores para ser usados en verilog y se     |
# | compara con los resultados obtenidos en coma flotante              |
# |____________________________________________________________________|                                                                                   

import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

lista_Sin       = []
lista_Cos       = []
lista_Sin_f_Max = []
lista_Cos_f_Max = []
lista_Sin_C_Max = []
lista_Cos_C_Max = []

N    = 4
frec = 1.0/((1.0/100.0e6)*N)

M = N

print(frec)

for t in range(M):
    valor = np.sin((2.0*np.pi*frec*(t/100.0e6)))  
    print("Seno: ",valor)
    lista_Sin.append(valor)

for t in range(M):
    valor = np.cos(2.0*np.pi*frec*(t/100.0e6))
    print("Cos: ",valor)
    lista_Cos.append(valor)

# ptr = 0
# for i in range (N): 
#     lista_Sin_f_Max.append(lista_Sin[ptr])    # Se recoje los valores max cada cuarto de vuelta
#     lista_Cos_f_Max.append(lista_Cos[ptr])
#     ptr += 256
#     if (ptr == N): break    


# print(lista_Sin_f_Max)
# print(lista_Cos_f_Max)

#____Cuantizado____#
lista_Sin = list(lista_Sin)
lista_Cos = list(lista_Cos)

lista_Sin_Cuanti = arrayFixedInt(8, 6, lista_Sin, signedMode='S', roundMode='round', saturateMode='saturate')
lista_Cos_Cuanti = arrayFixedInt(8, 6, lista_Cos, signedMode='S', roundMode='round', saturateMode='saturate')


for ptr in range(M):
    lista_Sin_Cuanti[ptr]   = lista_Sin_Cuanti[ptr].fValue
    lista_Cos_Cuanti[ptr]   = lista_Cos_Cuanti[ptr].fValue


print("SENO: ", lista_Sin_Cuanti)
print()
print("COSENO: ", lista_Cos_Cuanti)

##################################################################

# ptr = 0
# for i in range (N): 
#     lista_Sin_C_Max.append(lista_Sin_Cuanti[ptr])    # Se recoje los valores max cada cuarto de vuelta
#     lista_Cos_C_Max.append(lista_Cos_Cuanti[ptr])
#     ptr += 256
#     if (ptr == N): break  

#____Plot valores flotantes____#
plt.figure(figsize=[10,20])
plt.subplot(2,1,1)
plt.title('Seno Signal float')
plt.plot(lista_Sin, 'b-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.subplot(2,1,2)
plt.title('Coseno Signal float')
plt.plot(lista_Cos, 'r-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()

# plt.figure(figsize=[10,20])
# plt.subplot(2,1,1)
# plt.title('Seno Signal float')
# plt.plot(lista_Sin_f_Max, 'b.',linewidth=2.0)
# plt.grid(True)
# plt.xlabel('Muestras')
# plt.ylabel('Amplitud')
# plt.subplot(2,1,2)
# plt.title('Coseno Signal float')
# plt.plot(lista_Cos_f_Max, 'r.',linewidth=2.0)
# plt.grid(True)
# plt.xlabel('Muestras')
# plt.ylabel('Amplitud')
# plt.show()

#____Plot del cuantizado____#
plt.figure(figsize=[10,20])
plt.subplot(2,1,1)
plt.title('Seno Signal Cuanti')
plt.plot(lista_Sin_Cuanti, 'b-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.subplot(2,1,2)
plt.title('Coseno Signal Cuanti')
plt.plot(lista_Cos_Cuanti, 'r-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()

#____Plot Superpuestos____#
plt.figure(figsize=[10,20])
plt.subplot(2,1,1)
plt.title('Seno Signal Comparacion')
plt.plot(lista_Sin, 'r-',linewidth=5.0)
plt.plot(lista_Sin_Cuanti, 'b-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.subplot(2,1,2)
plt.title('Coseno Signal Comparacion')
plt.plot(lista_Cos, 'b-',linewidth=5.0)
plt.plot(lista_Cos_Cuanti, 'r-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()

# print()
# print("Valores maximos flotantes: ")
# print(lista_Sin_f_Max)
# print(lista_Cos_f_Max)
# print("Valores maximos cuantizados: ")
# print(lista_Sin_C_Max)
# print(lista_Cos_C_Max)