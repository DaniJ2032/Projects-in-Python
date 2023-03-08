# |_______________________SinyCosTab_V1.1b_____________________________|
# | Se grafica un periodo completo de un seno y un coseno tomando como |
# | frecuencia de muestreo 100Mhz lo cual la frec maxima a muestrear   |   
# | sera de 50Mhz segun el teorema de Nyquist.                         |      
# | Se busca realizar un muestreo de 1024 valores lo cual dara como    |
# | frecuencia minia a muestrear para 1024 sera:                       |
# | Tsampl = 1/100MHz --> 10ns                                         |
# | Tmuestras = 10ns * 1024muestras --> 10.24us                        | 
# | Frecmin = 1/10.24us --> 97.65625kHz                                |
# | Aparte se cuantiza los valores para ser usados en verilog y se     |
# | compara con los resultados obtenidos en coma flotante              |
# | ################################################################## |
# | NUEVO:                                                             |
# | Se toma 1024 valores en un cuarto de recorrido de 2Pi es decir     |
# | esto da como ventaja trabajar con el cuarto de onda obtenido y     |
# | espejando sus valores y negando se puede armar la onda sin y cos   |
# | completa generando asi 4096 datos dando como resultado una         |
# | una Frecmin = 24.4140625kHz                                        |
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

N           = 1024
frec        = 1.0/((1.0/100.0e6)*N)


print('La frecuencia es: ', frec)

for t in range(N):
    valor = np.sin((np.pi/2.0)*frec*(t/100.0e6))
    lista_Sin.append(valor)
 
for t in range(N):
    valor = np.cos((np.pi/2.0)*frec*(t/100.0e6))
    lista_Cos.append(valor)

#____Prubea de Espejado____#

#Sen
aux = lista_Sin[::-1]               # Se espeja primer cuarto (para hacer el 2do cuarto)
aux2 = [n * -1 for n in lista_Sin]  # Se niega primer cuarto (para hacer el 3er cuarto)
lista_Sin = lista_Sin + aux + aux2  # Se suma 1er, 2do y 3er cuarto    
aux2 = aux2[::-1]                   # Se espeja el 3er  cuarto (para hacer el 4to cuarto)
lista_Sin = lista_Sin + aux2        # Se suma el 4to cuarto y se completa la onda

aux.clear()
aux2.clear()

#Cos
aux = lista_Cos[::-1]               # Se espeja primer cuadrante (para hacer el 4to cuarto) 
aux2 = [n * -1 for n in aux]        # Se niega el espejado del primer cuadrante (para 2do cuarto)
lista_Cos = lista_Cos + aux2        # Se suma 1er y 2do cuarto
aux2 = aux2[::-1]                   # Se espeja 2do cuarto (para hacer el 3er cuarto)
lista_Cos = lista_Cos +  aux2 + aux # Se suma 3er y 4to cuarto completando la onda  

aux.clear()
aux2.clear()


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

#____Cuantizado____#
lista_Sin = list(lista_Sin)
lista_Cos = list(lista_Cos)
lista_Sin_Cuanti = arrayFixedInt(8, 6, lista_Sin, signedMode='S', roundMode='round', saturateMode='saturate')
lista_Cos_Cuanti = arrayFixedInt(8, 6, lista_Cos, signedMode='S', roundMode='round', saturateMode='saturate')

for ptr in range(len(lista_Sin)):
    lista_Sin_Cuanti[ptr]       = lista_Sin_Cuanti[ptr].fValue
    lista_Cos_Cuanti[ptr]       = lista_Cos_Cuanti[ptr].fValue

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
