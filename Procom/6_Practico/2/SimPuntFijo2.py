import os
import numpy as np
import Funtion as fun
import matplotlib.pyplot as plt
from tool._fixedInt import * 

#___________Parametros generales______________#
T     = 1.0/21.0e9  # Periodo de baudio
Nsymb = 511         # Numero de simbolos
os    = 4           # Over Sampling

## Parametros de la respuesta en frecuencia
Nfreqs = 256        # Cantidad de frecuencias

## Parametros del filtro de caida cosenoidal
beta   = 0.5        # Roll-Off
Nbauds = 6.0        # Cantidad de baudios del filtro

## Parametros funcionales
Ts = T/os           # Frecuencia de muestreo
########################################################3


#____Semillas para las PRBS_____
# PRBSI       =   [0, 1, 0, 1, 0, 1, 0, 1, 1] # --> Semilla cargada 0x1AA
PRBSI       =   [1, 1, 0, 1, 0, 1, 0, 1, 0] # --> Semilla cargada 0x1AA 110101010
PRBSQ       =   [0, 1, 1, 1, 1, 1, 1, 1, 1] # --> Semilla cargada 0x1FE
PRQ_List_to_FIR    =   []
PRQ_Out_to_Grafic  =   []

PRI_List_to_FIR    =   []
PRI_Out_to_Grafic  =   [] 

# generacion de valores para grafica y cuantizado de los coeficientes rc0
(t,rc0) = fun.rcosine(beta, T,os,Nbauds,Norm=False)
rc0 = fun.CUANTIZADO(rc0)

# FIRshiftRegQ    = np.zeros(len(rc0))    # --> sift reg del filtro fir
FIRshiftRegQ    = np.zeros(6)    # --> ShiftReg para polifasico
Out_FIR_Q       = []

# FIRshiftRegI    = np.zeros(len(rc0))    # --> sift reg del filtro fir
FIRshiftRegI    = np.zeros(6)    # --> ShiftReg para polifasico
Out_FIR_I       = []

beta            = 0.5
rc0aux          = []                    # --> Lista auxiliar

symb_out0Q          = []
symb_out0I          = []
symb_out0QAux       = []
symb_out0IAux       = []

#__________________Contador de BER____________________________#
BERShiftRegQ = np.zeros(1024)             # --> Doble de la secuencia generada por una PRBSQ
LatMinQ   = 1
countQ    = 0
posicionQ = 0
acum_out_FirQ = 0


BERShiftRegI = np.zeros(1024)             
LatMinI   = 1
countI    = 0
posicionI = 0
acum_out_FirI = 0
acumI =  []
acumQ =  []


# main principal
for j in range (1):
    for i in range (511): # BUSCAR MODULARIZAR TODO ESTE FOR 
        
        # PRBSQ
        auxQ        = PRBSQ   
        PRBSQ       = np.roll(PRBSQ, 1)       # --> roto 1 vez
        PRBSQ[0]    = (auxQ[4] ^ auxQ[8])     # --> xor entre los bits 4 y 8 

        if(PRBSQ[8] == 1): 
            PRQ_List_to_FIR.append(1)       # --> si es 1 lo conviero a -1
            PRQ_Out_to_Grafic.append(1)
            BERShiftRegQ[0] =  1
            auxPRQ = 1
        else :           
            PRQ_List_to_FIR.append(0)       # --> si es 0 lo convierto a 1
            PRQ_Out_to_Grafic.append(0)   
            BERShiftRegQ[0]  = 0 
            auxPRQ  = 0
        # PRBSI
        auxI        = PRBSI
   
        PRBSI       = np.roll(PRBSI, 1)       # --> roto 1 vez
        PRBSI[0]    = (auxI[4] ^ auxI[8])     # --> xor entre los bits 4 y 8 
        if(PRBSI[8] == 1): 
            PRI_List_to_FIR.append(1)       # --> si es 1 lo conviero a -1
            PRI_Out_to_Grafic.append(1)

            BERShiftRegI[0] =  1
            auxPRI = 1
        else :           
            PRI_List_to_FIR.append(0)       # --> si es 0 lo convierto a 1
            PRI_Out_to_Grafic.append(0) 

            BERShiftRegI[0] = 0 
            auxPRI  = 0
#########################################        HACER POLIFASICO 

        for i in range(os - 1):
            PRI_List_to_FIR.append(0)    #Sobremuestreo
            PRQ_List_to_FIR.append(0)
        
        FIRshiftRegI    = np.roll(FIRshiftRegI,1)
        FIRshiftRegI[0] = auxPRI
        FIRshiftRegQ    = np.roll(FIRshiftRegQ,1)
        FIRshiftRegQ[0] = auxPRQ
        
        for entrada_mux in range(4):
            indice = entrada_mux
            for num_mux in range(6):
                salida_mux = rc0[indice]
                if (FIRshiftRegI[num_mux] == 0):
                    acum_out_FirI += salida_mux
                else:
                    acum_out_FirI += -(salida_mux)
                
                if (FIRshiftRegQ[num_mux] == 0):
                    acum_out_FirQ += salida_mux
                else:
                    acum_out_FirQ += -(salida_mux)
                indice += 4
            aux_symb_outI = acum_out_FirI
            aux_symb_outQ = acum_out_FirQ
            acum_out_FirI = 0
            acum_out_FirQ = 0
            symb_out0I.append(aux_symb_outI)
            symb_out0Q.append(aux_symb_outQ)

            if (entrada_mux == 0):

                symb_out0IAux.append(aux_symb_outI)
                symb_out0QAux.append(aux_symb_outQ)

                if aux_symb_outI >= 0:
                    slicerI = 0
                else:
                    slicerI = 1

                countI = countI + (slicerI ^ int(BERShiftRegI[j]))
                
                if aux_symb_outQ >= 0:
                    slicerQ = 0
                else:
                    slicerQ = 1
                countQ = countQ + (slicerQ ^ int(BERShiftRegQ[j]))

#########################################
    acumI.append(countI)
    acumQ.append(countQ)
    # Comparacion para encontrar el minimo valor en una posicion de la BER


    if (countQ < LatMinQ):
        LatMinQ = countQ
        print("Latencia minima Q: ",j)

    if (countI < LatMinI):
        LatMinI = countI
        print("Latencia minima I: ",j)

    #Reseteo de varaibles para las graficas
    if (j == 1022): 
        Out_FIR_Q           .clear()
        PRQ_Out_to_Grafic   .clear()
        Out_FIR_I           .clear()
        PRI_Out_to_Grafic   .clear()   
        symb_out0Q          .clear()
        symb_out0I          .clear()
        symb_out0QAux       .clear()
        symb_out0IAux       .clear()     

    countQ = 0 
    countI = 0


symb_out0Q  = np.array(symb_out0Q)
PRQ_Out_to_Grafic   = np.array(PRQ_Out_to_Grafic)   # --> obtengo el dato de salida Q
symbolsQ    = PRQ_Out_to_Grafic

symb_out0I  = np.array(symb_out0I)
PRI_Out_to_Grafic   = np.array(PRI_Out_to_Grafic)   # --> obtengo el dato de salida I
symbolsI = PRI_Out_to_Grafic  # Salidas de la PRBS para la grafica

symb_out0QAux = np.array(symb_out0QAux)
symb_out0IAux = np.array(symb_out0IAux)

#Cuantizacion de datos de salida
symb_out0Q       = arrayFixedInt(8, 6, symb_out0Q, signedMode='S', roundMode='trunc', saturateMode='saturate')
symb_out0I       = arrayFixedInt(8, 6, symb_out0I, signedMode='S', roundMode='trunc', saturateMode='saturate')
symb_out0QAux    = arrayFixedInt(8, 6, symb_out0QAux, signedMode='S', roundMode='trunc', saturateMode='saturate')
symb_out0IAux    = arrayFixedInt(8, 6, symb_out0IAux, signedMode='S', roundMode='trunc', saturateMode='saturate')


for ptr in range(len(symb_out0Q)):
    symb_out0Q[ptr] = symb_out0Q[ptr].fValue
    symb_out0I[ptr] = symb_out0I[ptr].fValue 

for ptr in range(len(symb_out0QAux)):
    symb_out0QAux[ptr]  = symb_out0QAux[ptr].fValue
    symb_out0IAux[ptr]  = symb_out0IAux[ptr].fValue 

# for i in range (30):
#     print(symbolsI[i])


#________________________Graficos_____________________________#

# plt.figure(figsize=[14,7])
# plt.plot(t,rc0,'ro-',linewidth=2.0,label=r'$\beta=0.5$')
# plt.legend()
# plt.grid(True)
# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')

# symb00    = np.zeros(int(os)*3+1);symb00[4:len(symb00)-1:int(os)] = 1.0
# rc0Symb00 = np.convolve(rc0,symb00)

# plt.figure(figsize=[14,7])
# plt.subplot(3,1,1)
# plt.plot(np.arange(0,len(rc0)),rc0,'r.-',linewidth=2.0,label=r'$\beta=0.5$')
# plt.plot(np.arange(4,len(rc0)+4),rc0,'k.-',linewidth=2.0,label=r'$\beta=0.5$')
# plt.stem(np.arange(12,len(symb00)+12),symb00,label='Bits',use_line_collection=True)
# plt.plot(rc0Symb00[4::],'--',linewidth=3.0,label='Convolution')
# plt.legend()
# plt.grid(True)
# plt.xlim(0,35)
# plt.ylim(-0.2,1.4)
# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')
# plt.title('Rcosine - OS: %d'%int(os))
# plt.show()
# #////////////////////////////////


# #Calculo respuesta en frec para los tres pulsos
# [H0,A0,F0] = fun.resp_freq(rc0, Ts, Nfreqs)
# # Generacion de los graficos para la respuesta en frecuencia
# plt.figure(figsize=[14,6])
# plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.5$')
# # plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
# # plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
# # plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
# plt.legend(loc=3)
# plt.grid(True)
# plt.xlim(F0[1],F0[len(F0)-1])
# plt.xlabel('Frequencia [Hz]')
# plt.ylabel('Magnitud [dB]')
# plt.show()
# #////////////////////////////////////


# #Grafica de distribucion de simbolos 

# label = 'Simbolos: %d' % Nsymb
# plt.figure(figsize=[14,6])
# plt.subplot(1,2,1)
# plt.hist(symbolsI,label=label)
# plt.legend()
# plt.xlabel('Simbolos')
# plt.ylabel('Repeticiones')
# plt.subplot(1,2,2)
# plt.hist(symbolsQ,label=label)
# plt.legend()
# plt.xlabel('Simbolos')
# plt.ylabel('Repeticiones')
# plt.show()
# #/////////////////////////////////


# #Grafia de simbolos transmitidos

# plt.figure(figsize=[10,6])
# plt.subplot(2,1,1)
# plt.plot(PRI_Out_to_Grafic,'o')
# plt.xlim(0,100)
# plt.grid(True)
# plt.subplot(2,1,2)
# plt.plot(PRQ_Out_to_Grafic,'o')
# plt.xlim(0,100)
# plt.grid(True)
# plt.show()
# #//////////////////////////////////


# #Grafica de respuesta a la convolucion      REVISAR¡¡¡¡¡¡¡¡¡¡¡¡¡
# # symb_out0I = np.convolve(rc0,zsymbI,'full')
# # symb_out0Q = np.convolve(rc0,zsymbQ,'full')

# for i in range (10):
#     print(symb_out0I[i])
# print()
# print()
# for i in range (10):
#     print(symb_out0Q[i])

# plt.figure(figsize=[10,6])
# plt.subplot(2,1,1)
# plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
# plt.xlim(0,200)
# plt.grid(True)
# plt.legend()
# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')

# plt.subplot(2,1,2)
# plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
# plt.xlim(0,200)
# plt.grid(True)
# plt.legend()
# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')

# plt.figure(figsize=[10,6])

# for i in range (len (PRI_Out_to_Grafic)):
#     if PRI_Out_to_Grafic[i] == 0: PRI_Out_to_Grafic[i] = 1 
#     else: PRI_Out_to_Grafic[i] = -1
# plt.plot(np.correlate(symb_out0IAux,PRI_Out_to_Grafic,'same'))
# plt.show()
# #////////////////////////////////////////

# #Grafica de diagrama ojo
# fun.eyediagram(symb_out0I[100:len(symb_out0I)-100],os,5,Nbauds)
# fun.eyediagram(symb_out0Q[100:len(symb_out0Q)-100],os,5,Nbauds)
#///////////////////////////

#Grafica de constelacion 
offset = 8

Xrvec = []
Xivec = []

# ####FUNCIONA? ROTACION DE SIMBOLOS......
# for i in range (len(symb_out0Q)):
#     Xrvec.append((symb_out0I[i] * np.sin((i)) +  symb_out0Q[i] * np.cos((i))))
#     Xivec.append((symb_out0I[i] * np.cos((i)) -  symb_out0Q[i] * np.sin((i))))   

# Xrvec             = np.array(Xrvec)
# Xivec             = np.array(Xivec)


plt.figure(figsize=[6,6])
plt.plot(symb_out0I[100+offset:len(symb_out0I)-(100-offset):int(os)],
         symb_out0Q[100+offset:len(symb_out0Q)-(100-offset):int(os)],
             '.',linewidth=2.0)

plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.show()
#///////////////////////////
  