# |_______________________SinyCosTab_V1_2b_____________________________|
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
# | ###################################################################|
# | NUEVO:                                                             |
# | Simulacion de multiplexores para el armado de la onda completa     |
# | para posterior uso en verilog                                      |
# |____________________________________________________________________|  
import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

lista_Sin        = []
lista_Cos        = []
lista_Sin_mux    = []   #Prueba para mux
lista_Cos_mux    = []
lista_Sin_Cuanti = []
lista_Cos_Cuanti = []


MUESTRAS    = 1024
frec        = 1.0/((1.0/100.0e6)*MUESTRAS)

DENOMINADOR = MUESTRAS//(2**0)
PASO = (MUESTRAS//DENOMINADOR)

RECORRIDO = (MUESTRAS*4)


print('paso: ', PASO)
print()

# print('La frecuencia es: ', frec)

for t in range(MUESTRAS):
    valor = np.sin((np.pi/2.0)*frec*(t/100.0e6))
    lista_Sin.append(valor)
 
for t in range(MUESTRAS):
    valor = np.cos((np.pi/2.0)*frec*(t/100.0e6))
    lista_Cos.append(valor)

#____mux de uso de mux para generar onda completa Seno____# #OK
n = 0
              
for j in range(3):
    for i in range(RECORRIDO//PASO):
        if (i < (1024//PASO)):                           # 1er mux           
            lista_Sin_mux.append(lista_Sin[n])           # Se recorre la lista normalmente hasta el ultimo valor
            if  ((PASO-1) == 0): n = n + PASO
            if  ((PASO-1) != 0): n = n + (PASO-1)  


        if (i >= (1024//PASO) and i < (2048//PASO)):     # 2do mux                     
            if  ((PASO-1) == 0): n = n - PASO            # Ahora se recorre la lista en sentido inverso (2do cuarto)   
            lista_Sin_mux.append(lista_Sin[n])          
            if  ((PASO-1) != 0): n = n - (PASO-1)                              

        if (i >= (2048//PASO) and i < (3072//PASO)):    # 3er mux              
            lista_Sin_mux.append(lista_Sin[n]*-1)       # Se vuelve a recorrer en sentido normal pero negando los valores (3er cuarto)  
            if  ((PASO-1) == 0): n = n + PASO              
            if  ((PASO-1) != 0): n = n + (PASO-1)


        if (i >= (3072//PASO) and i < (4096//PASO) ):    # 4to mux          
            if  ((PASO-1) == 0): n = n - PASO            # por ultimo se recorre en sentido inverso y negando valores (4to cuarto)           
            lista_Sin_mux.append(lista_Sin[n]*-1)       
            if  ((PASO-1) != 0): n = n - (PASO-1)                                       


#____mux de uso de mux para generar onda completa Cos____#
    n = 0
    for i in range(RECORRIDO//PASO):

        if (i < (1024//PASO)):                          # 1er mux
            lista_Cos_mux.append(lista_Cos[n])          # Se recorre la lista normalmente hasta el ultimo valor
            if  ((PASO-1) == 0): n = n + PASO
            if  ((PASO-1) != 0): n = n + (PASO-1)

        if (i > (1023//PASO) and i < (2048//PASO)):     # 2do mux
            if  ((PASO-1) == 0): n = n - PASO             
            lista_Cos_mux.append(lista_Cos[n]*-1)       # Ahora se recorre la lista en sentido inverso y se niega los valores (2do cuarto) 
            if  ((PASO-1) != 0): n = n - (PASO-1)                                  
    
        if (i > (2047//PASO) and i < (3072//PASO)):     # 3er mux                                                                                                  
            lista_Cos_mux.append(lista_Cos[n]*-1)       # Se recorrer en sentido normal y negando los valores (3er cuarto)       
            if  ((PASO-1) == 0): n = n + PASO              
            if  ((PASO-1) != 0): n = n + (PASO-1)

        if (i > (3071//PASO) and i < (4096//PASO) ):    # 4to mux
            if  ((PASO-1) == 0): n = n - PASO           
            lista_Cos_mux.append(lista_Cos[n])          # por ultimo se recorre en sentido inverso (4to cuarto)
            if  ((PASO-1) != 0): n = n - (PASO-1)                                 
       

#____Cuantizado____#
lista_Sin_mux = list(lista_Sin_mux)
lista_Cos_mux = list(lista_Cos_mux)
lista_Sin_Cuanti = arrayFixedInt(8, 6, lista_Sin_mux, signedMode='S', roundMode='round', saturateMode='saturate')
lista_Cos_Cuanti = arrayFixedInt(8, 6, lista_Cos_mux, signedMode='S', roundMode='round', saturateMode='saturate')

for ptr in range(len(lista_Sin_Cuanti)):
    lista_Sin_Cuanti[ptr]       = lista_Sin_Cuanti[ptr].fValue
    lista_Cos_Cuanti[ptr]       = lista_Cos_Cuanti[ptr].fValue

#____Plot valores flotantes____#
plt.figure(figsize=[10,20])
plt.subplot(2,1,1)
plt.title('Seno Signal float')
plt.plot(lista_Sin_mux, 'b-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.subplot(2,1,2)
plt.title('Coseno Signal float')
plt.plot(lista_Cos_mux, 'r-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()

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
plt.plot(lista_Sin_mux, 'r-',linewidth=5.0)
plt.plot(lista_Sin_Cuanti, 'b-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.subplot(2,1,2)
plt.title('Coseno Signal Comparacion')
plt.plot(lista_Cos_mux, 'b-',linewidth=5.0)
plt.plot(lista_Cos_Cuanti, 'r-',linewidth=2.0)
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.show()