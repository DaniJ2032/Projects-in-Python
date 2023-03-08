# |_________________________TP Integrador Simulacion en python ____________________________|
# | Autor: Juarez Daniel, Jose Gomez Lazarte                                               |         
# | Año: 2023                                                                              |         
# | Nombre: TPIntegradorSimulador 1.0b                                                     |             
# | Descripcion:                                                                           | 
# |             Este script se simula el comportamiento del filtro en la FPGA teninendo    |
# | en cuneta que en las simulaciones las latencias son nulas. Se modela el comportamiento |
# | del filtro en conjunto con la PRBS y al ber como si se estuviera en la FPGA, lo que si |
# | en la verdadera implementacion no se logro obtener a nivel de sofware el offset con el |
# | que se capturo los datos debido a las latencias propias del sistema, situacion que en  |
# | este simulador no ocurre por eso se lo ve implementado. Se espera en un futuro poder   |
# | mejorarlo para que se pueda encontrar un offset de manera automatica desde la FPGA     |
# |________________________________________________________________________________________|

import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *
import SInyCosTab2 as tabla 

#___Variables para simlacion de DSP___#
os             = 4                              # OverSampling
beta           = 0.5                            # Beta                             
Nsymb          = 511                            # Numero de simbolos
T              = 1.0/100e6                      # Periodo de baudio
Ts             = T/os                           # Frecuencia de muestreo
Nfreqs         = 256                            # Cantidad de frecuencias
Nbauds         = 6.0                            # Cantidad de baudios del filtro
PRBSI          = np.array ([1,1,0,1,0,1,0,1,0]) # PRBSI Seed
PRBSQ          = np.array ([1,1,1,1,1,1,1,1,0]) # PRBSQ Seed

SR1            = np.array ([0,0,0,0,0,0])       # Salidas de Signo del FiltroI
SR2            = np.array ([0,0,0,0,0,0])       # Salidas de Signo del FiltroQ

coeficientes   = np.array ( 
    [ 8.95103186e-34,  4.77279499e-03,  1.71488822e-02,  2.27496429e-02,    # Coeficienes del Cos realzado en
    -1.54351892e-16, -5.76127319e-02, -1.20042175e-01, -1.22501738e-01,     # coma flotante
    1.60734027e-15,  2.62503724e-01,  6.00210877e-01,  8.87236072e-01,
    1.00000000e+00,  8.87236072e-01,  6.00210877e-01,  2.62503724e-01,
    -2.94478863e-15, -1.22501738e-01, -1.20042175e-01, -5.76127319e-02,
    7.40915352e-16,  2.27496429e-02,  1.71488822e-02,  4.77279499e-03] 
                           )

berQ                = np.zeros(1024)
berI                = np.zeros(1024)
salidaPRBSI         = []
salidaPRBSQ         = []
salidaPRBSI_sinOS   = []             
salidaPRBSQ_sinOS   = []                
PRBSI_AUX           = []
PRBSQ_AUX           = []
symb_out0Q          = []
symb_out0I          = []
symb_out0I_sinOS    = []
symb_out0Q_sinOS    = []
acumulador_arregloQ = []
acumulador_arregloI = []

contador_berI             = 0
contador_berQ             = 0
acumulador_salida_filtroI = 0
acumulador_salida_filtroQ = 0

#____Cuantizado de los coeficientes del filtro____#
coeficientes = arrayFixedInt(8, 6, coeficientes, signedMode='S', roundMode='round', saturateMode='saturate')
for ptr in range(len(coeficientes)):
    coeficientes[ptr] = coeficientes[ptr].fValue
coeficientes = coeficientes.tolist()   

for j in range(3):
    for i in range(511):

        #___PRBSI___#
        berI     = np.roll(berI,1)
        PRBSI    = np.roll(PRBSI,1)         
        PRBSI[0] = PRBSI[0] ^ PRBSI[5]
        PRBSI_AUX.append(PRBSI[8])
        if PRBSI[8] == 0:
            berI[0] =  0
            salidaPRBSI.append(0)
            salidaPRBSI_sinOS.append(0)
            SalidaPRBSI_actual = 0
        else:
            berI[0] =  1
            salidaPRBSI.append(1)
            salidaPRBSI_sinOS.append(1)
            SalidaPRBSI_actual = 1

        #___PRBSQ___#
        berQ = np.roll(berQ,1)
        PRBSQ    = np.roll(PRBSQ,1)
        PRBSQ[0] = PRBSQ[0] ^ PRBSQ[5]
        PRBSQ_AUX.append(PRBSQ[8])
        if PRBSQ[8] == 0:
            berQ[0] =  0
            salidaPRBSQ.append(0)
            salidaPRBSQ_sinOS.append(0)
            SalidaPRBSQ_actual = 0
        else:
            berQ[0] =  1
            salidaPRBSQ.append(1)
            salidaPRBSQ_sinOS.append(1)
            SalidaPRBSQ_actual = 1

        #___Sobremuestreo___#
        for i in range(os - 1):
            salidaPRBSI.append(0)    
            salidaPRBSQ.append(0)

        #___Toma del signo de los datos a la salida de los filtros___#
        SR1    = np.roll(SR1,1)
        SR1[0] = SalidaPRBSI_actual
        SR2    = np.roll(SR2,1)
        SR2[0] = SalidaPRBSQ_actual
        
        #___Simulacion de filtro polifasico___#
        for entrada_mux in range(4):
            indice = entrada_mux
            for num_mux in range(6):
                salida_mux = coeficientes[indice]
                if (SR1[num_mux] == 0):
                    acumulador_salida_filtroI += salida_mux
                else:
                    acumulador_salida_filtroI += -(salida_mux)
                
                if (SR2[num_mux] == 0):
                    acumulador_salida_filtroQ += salida_mux
                else:
                    acumulador_salida_filtroQ += -(salida_mux)
                indice += 4

            aux_symb_outI = acumulador_salida_filtroI
            aux_symb_outQ = acumulador_salida_filtroQ

            acumulador_salida_filtroI = 0
            acumulador_salida_filtroQ = 0           

            #___Salida de 4 datos por filtro en cada ciclo de relog___#
            symb_out0I.append(aux_symb_outI)
            symb_out0Q.append(aux_symb_outQ)
            
            #___Slizer  y contador de BERQ e I___#
            if (entrada_mux == 0):

                symb_out0I_sinOS.append(aux_symb_outI)
                symb_out0Q_sinOS.append(aux_symb_outQ)

                if aux_symb_outI >= 0:
                    slicerI = 0
                else:
                    slicerI = 1
                contador_berI = contador_berI + (slicerI ^ int(berI[j]))
                
                if aux_symb_outQ >= 0:
                    slicerQ = 0
                else:
                    slicerQ = 1
                contador_berQ = contador_berQ + (slicerQ ^ int(berQ[j]))
                
    #___Busqueda de la latencia minima___#
    acumulador_arregloI.append(contador_berI)
    if (contador_berI == 0):
        print("Latencia minima en I:",j) 
    
    acumulador_arregloQ.append(contador_berQ)
    if (contador_berQ == 0):
        print("Latencia minima en Q:",j)
           
    #___Reseteo de variables___#
    if (j == 1022):
        salidaPRBSI      .clear()
        salidaPRBSQ      .clear()
        salidaPRBSI_sinOS.clear()
        salidaPRBSQ_sinOS.clear()
        PRBSI_AUX        .clear()
        PRBSQ_AUX        .clear()
        symb_out0Q       .clear()
        symb_out0I       .clear()
        symb_out0I_sinOS .clear()
        symb_out0Q_sinOS .clear()
    
    contador_berI = 0
    contador_berQ = 0       

#___Cuantizado de datos a la salida del las BER'S___#       
symb_out0Q       = arrayFixedInt(8, 6, symb_out0Q, signedMode='S', roundMode='round', saturateMode='saturate')
symb_out0I       = arrayFixedInt(8, 6, symb_out0I, signedMode='S', roundMode='round', saturateMode='saturate')
symb_out0Q_sinOS = arrayFixedInt(8, 6, symb_out0Q_sinOS, signedMode='S', roundMode='round', saturateMode='saturate')
symb_out0I_sinOS = arrayFixedInt(8, 6, symb_out0I_sinOS, signedMode='S', roundMode='round', saturateMode='saturate')


for ptr in range(len(symb_out0Q)):
    symb_out0Q[ptr]       = symb_out0Q[ptr].fValue
    symb_out0I[ptr]       = symb_out0I[ptr].fValue

for ptr in range(len(symb_out0Q_sinOS)):    
    symb_out0Q_sinOS[ptr] = symb_out0Q_sinOS[ptr].fValue 
    symb_out0I_sinOS[ptr] = symb_out0I_sinOS[ptr].fValue  

#__Generacion de ruido___#
# noiseI = (np.random.uniform(0, 0.1, np.size(symb_out0I)))    
# noiseQ = (np.random.uniform(0, 0.1, np.size(symb_out0I)))

#___Ruido montado en ambas salidas___#
# symb_out0Q = symb_out0Q + noiseQ
# symb_out0I = symb_out0I + noiseI                           

#___Simulacion de rotacion de constelacion de simbolos transmitidos debido a ruido de fase___#


#___Variables para la rotacion de simbolos___#
Xrvec   =   []
Xivec   =   []
MUESTRAS    = 1024
DENOMINADOR = (MUESTRAS//(2**0))
PASO = (MUESTRAS//DENOMINADOR) 
RECORRIDO = (MUESTRAS*4)
##############################################
base = 0   # Simulacion de logue de cualquier posicion de los datos a la salida del filtro 
ptrWave = 0       
offset = 0
offsetRot = 0
print("Cantidad de pasos: ", PASO)

lista_sin_mux = []
lista_cos_mux = []

for j in range (3):
    for i in range (RECORRIDO//PASO):
        if (i < (1024//PASO)):                          # 1er mux
            lista_sin_mux.append(tabla.lista_Sin[ptrWave])
            lista_cos_mux.append(tabla.lista_Cos[ptrWave])        
            if  ((PASO-1) == 0):  ptrWave = ptrWave + PASO
            if  ((PASO-1) != 0):  ptrWave = ptrWave + (PASO-1)  

        if (i >= (1024//PASO) and i < (2048//PASO)):     # 2do mux
            if  ((PASO-1) == 0): ptrWave = ptrWave - PASO
            lista_sin_mux.append(tabla.lista_Sin[ptrWave])
            lista_cos_mux.append(-tabla.lista_Cos[ptrWave])        
            if  ((PASO-1) != 0): ptrWave = ptrWave - (PASO-1)                              

        if (i >= (2048//PASO) and i < (3072//PASO)):     # 3er mux
            lista_sin_mux.append(-tabla.lista_Sin[ptrWave])
            lista_cos_mux.append(-tabla.lista_Cos[ptrWave])        
            if  ((PASO-1) == 0): ptrWave = ptrWave + PASO              
            if  ((PASO-1) != 0): ptrWave = ptrWave + (PASO-1)

        if (i >= (3072//PASO) and i < (4096//PASO) ):    # 4to mux
            if  ((PASO-1) == 0): ptrWave = ptrWave - PASO 
            lista_sin_mux.append(-tabla.lista_Sin[ptrWave])
            lista_cos_mux.append(tabla.lista_Cos[ptrWave])        
            if  ((PASO-1) != 0): ptrWave = ptrWave - (PASO-1) 
ptrWave = 0
   
for ptrSig in range (900):
    Xrvec.append((symb_out0I[ptrSig + base] * lista_cos_mux[ptrWave]) - (symb_out0Q[ptrSig + base] * lista_sin_mux[ptrWave]))
    Xivec.append((symb_out0I[ptrSig + base] * lista_sin_mux[ptrWave]) + (symb_out0Q[ptrSig + base] * lista_cos_mux[ptrWave]))   
    if(ptrWave == len(lista_cos_mux) - 1): ptrWave = 0 
    else: ptrWave += 1  


Xrvec = arrayFixedInt(8, 6, Xrvec, signedMode='S', roundMode='round', saturateMode='saturate')
Xivec = arrayFixedInt(8, 6, Xivec, signedMode='S', roundMode='round', saturateMode='saturate')

for ptr in range(len(Xrvec)):
    Xrvec[ptr]  = Xrvec[ptr].fValue
    Xivec[ptr]  = Xivec[ptr].fValue

salidaPRBSI         = np.array( salidaPRBSI       )
salidaPRBSQ         = np.array( salidaPRBSQ       )
salidaPRBSI_sinOS   = np.array( salidaPRBSI_sinOS )
salidaPRBSQ_sinOS   = np.array( salidaPRBSQ_sinOS )
PRBSI_AUX           = np.array( PRBSI_AUX         )
PRBSQ_AUX           = np.array( PRBSQ_AUX         )
symb_out0Q          = np.array( symb_out0Q        )
symb_out0I          = np.array( symb_out0I        )
symb_out0I_sinOS    = np.array( symb_out0I_sinOS  )
symb_out0Q_sinOS    = np.array( symb_out0Q_sinOS  )

#____Graficos de las salidas____#

#___Salidas del filtro pre rotado
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(0,300)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(0,300)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#___Salidas del filtro post rotado
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(Xrvec,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(0,200)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(Xivec,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(0,200)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

#____Salida de los Senos y cosenos
plt.figure(figsize=[10,20])
plt.subplot(2,1,1)
plt.title('Seno Signal float')
plt.plot(lista_sin_mux, 'b-',linewidth=2.0)

plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')
plt.subplot(2,1,2)
plt.title('Coseno Signal float')
plt.plot(lista_cos_mux, 'r-',linewidth=2.0)

plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Amplitud')

#____Grafico de constelacion Sin rotar
plt.figure(figsize=[6,6])
plt.plot(symb_out0I[offset:len(symb_out0I)-offset:int(os)], 
symb_out0Q[offset:len(symb_out0Q)-offset:int(os)], '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

#____Grafico de constelacion rotado
plt.figure(figsize=[6,6])
plt.plot(Xrvec[offsetRot:len(Xrvec)-offsetRot:int(os)], 
         Xivec[offsetRot:len(Xivec)-offsetRot:int(os)], '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')

plt.show()