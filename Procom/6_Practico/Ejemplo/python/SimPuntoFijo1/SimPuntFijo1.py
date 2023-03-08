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
PRBSI       =   [0, 1, 0, 1, 0, 1, 0, 1, 1] # --> Semilla cargada 0x1AA
PRBSQ       =   [0, 1, 1, 1, 1, 1, 1, 1, 1] # --> Semilla cargada 0x1FE
PRQ_List_to_FIR    =   []
PRQ_Out_to_Grafic  =   []

PRI_List_to_FIR    =   []
PRI_Out_to_Grafic  =   [] 

# generacion de valores para grafica y cuantizado de los coeficientes rc0
(t,rc0) = fun.rcosine(beta, T,os,Nbauds,Norm=False)
rc0 = fun.CUANTIZADO(rc0)

FIRshiftRegQ    = np.zeros(len(rc0))    # --> sift reg del filtro fir
Out_FIR_Q       = []

FIRshiftRegI    = np.zeros(len(rc0))    # --> sift reg del filtro fir
Out_FIR_I       = []

beta            = 0.5
rc0aux          = []                    # --> Lista auxiliar


#__________________Contador de BER____________________________#
BERShiftRegQ = np.zeros(1024)             # --> Doble de la secuencia generada por una PRBSQ
LatMinQ   = 1
countQ    = 0
posicionQ = 0

BERShiftRegI = np.zeros(1024)             
LatMinI   = 1
countI    = 0
posicionI = 0

# main principal
for j in range (1):
    for i in range (Nsymb): # BUSCAR MODULARIZAR TODO ESTE FOR 

        # PRBSQ
        auxQ        = PRBSQ   
        PRBSQ       = np.roll(PRBSQ, 1)       # --> roto 1 vez
        PRBSQ[0]    = (auxQ[4] ^ auxQ[8])     # --> xor entre los bits 4 y 8 

        if(PRBSQ[8] == 1): 
            PRQ_List_to_FIR.append(-1)       # --> si es 1 lo conviero a -1
            PRQ_Out_to_Grafic.append(-1)
            BERauxQ =  1
            auxPRQ = -1
        else :           
            PRQ_List_to_FIR.append(1)       # --> si es 0 lo convierto a 1
            PRQ_Out_to_Grafic.append(1)   
            BERauxQ  = 0 
            auxPRQ  = 1
        # PRBSI
        auxI        = PRBSI   
        PRBSI       = np.roll(PRBSI, 1)       # --> roto 1 vez
        PRBSI[0]    = (auxI[4] ^ auxI[8])     # --> xor entre los bits 4 y 8 

        if(PRBSI[8] == 1): 
            PRI_List_to_FIR.append(-1)       # --> si es 1 lo conviero a -1
            PRI_Out_to_Grafic.append(-1)
            BERauxI =  1
            auxPRI = -1
        else :           
            PRI_List_to_FIR.append(1)       # --> si es 0 lo convierto a 1
            PRI_Out_to_Grafic.append(1)   
            BERauxI  = 0 
            auxPRI  = 1
################################

        # Filtro FIRQ    
        FIRshiftRegQ      =   np.roll(FIRshiftRegQ, 1) # --> roto una vez
        FIRshiftRegQ[0]   =   auxPRQ
        FirQ = np.dot(FIRshiftRegQ, rc0)
        Out_FIR_Q.append(FirQ)     

        #La salida del FIR pasa por un Zlizer, detectamos el signo del dato
        if  (FirQ >= 0): auxFIRQ = 0 
        else:            auxFIRQ = 1           

        # Filtro FIRI    
        FIRshiftRegI      =   np.roll(FIRshiftRegI, 1) # --> roto una vez
        FIRshiftRegI[0]   =   auxPRI
        FirI = np.dot(FIRshiftRegI, rc0)
        Out_FIR_I.append(FirI)     

        #La salida del FIR pasa por un Zlizer, detectamos el signo del dato
        if  (FirI >= 0): auxFIRI = 0 
        else:            auxFIRI = 1
#################################

        # Contador de BERI
        BERShiftRegI = np.roll(BERShiftRegI, 1) # --> roto una vez
        BERShiftRegI[0] = BERauxI
        countI   = countI + (auxFIRI ^ int(BERShiftRegI[j])) # --> acumulo la cuenta 

        # Contador de BERQ
        BERShiftRegQ = np.roll(BERShiftRegQ, 1) # --> roto una vez
        BERShiftRegQ[0] = BERauxQ
        countQ   = countQ + (auxFIRQ ^ int(BERShiftRegQ[j])) # --> acumulo la cuenta 
#################################

        # 2da vuelta del FIRQ con el sobremuestreo
        for m in range (os-1):    
            PRI_List_to_FIR.append(0)        
            FIRshiftRegI      =   np.roll(FIRshiftRegI, 1) # --> roto una vez
            FIRshiftRegI[0]   =   0
            FirI = np.dot(FIRshiftRegI, rc0)
            Out_FIR_I.append(FirI)  

        for m in range (os-1):    
            PRQ_List_to_FIR.append(0)        
            FIRshiftRegQ      =   np.roll(FIRshiftRegQ, 1) # --> roto una vez
            FIRshiftRegQ[0]   =   0
            FirQ = np.dot(FIRshiftRegQ, rc0)
            Out_FIR_Q.append(FirQ)
#########################################

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

    countQ = 0 
    countI = 0


symb_out0Q  = np.array(Out_FIR_Q)
PRQ_Out_to_Grafic   = np.array(PRQ_Out_to_Grafic)   # --> obtengo el dato de salida Q
symbolsQ    = PRQ_Out_to_Grafic

symb_out0I  = np.array(Out_FIR_I)
PRI_Out_to_Grafic   = np.array(PRI_Out_to_Grafic)   # --> obtengo el dato de salida I
symbolsI = PRI_Out_to_Grafic  # Salidas de la PRBS para la grafica



#________________________Graficos_____________________________#

plt.figure(figsize=[14,7])
plt.plot(t,rc0,'ro-',linewidth=2.0,label=r'$\beta=0.5$')
plt.legend()
plt.grid(True)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

symb00    = np.zeros(int(os)*3+1);symb00[4:len(symb00)-1:int(os)] = 1.0
rc0Symb00 = np.convolve(rc0,symb00)

plt.figure(figsize=[14,7])
plt.subplot(3,1,1)
plt.plot(np.arange(0,len(rc0)),rc0,'r.-',linewidth=2.0,label=r'$\beta=0.5$')
plt.plot(np.arange(4,len(rc0)+4),rc0,'k.-',linewidth=2.0,label=r'$\beta=0.5$')
plt.stem(np.arange(12,len(symb00)+12),symb00,label='Bits',use_line_collection=True)
plt.plot(rc0Symb00[4::],'--',linewidth=3.0,label='Convolution')
plt.legend()
plt.grid(True)
plt.xlim(0,35)
plt.ylim(-0.2,1.4)
plt.xlabel('Muestras')
plt.ylabel('Magnitud')
plt.title('Rcosine - OS: %d'%int(os))
plt.show()
#////////////////////////////////


#Calculo respuesta en frec para los tres pulsos
[H0,A0,F0] = fun.resp_freq(rc0, Ts, Nfreqs)
# Generacion de los graficos para la respuesta en frecuencia
plt.figure(figsize=[14,6])
plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.5$')
# plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
# plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
# plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
plt.legend(loc=3)
plt.grid(True)
plt.xlim(F0[1],F0[len(F0)-1])
plt.xlabel('Frequencia [Hz]')
plt.ylabel('Magnitud [dB]')
plt.show()
#////////////////////////////////////


#Grafica de distribucion de simbolos 

label = 'Simbolos: %d' % Nsymb
plt.figure(figsize=[14,6])
plt.subplot(1,2,1)
plt.hist(symbolsI,label=label)
plt.legend()
plt.xlabel('Simbolos')
plt.ylabel('Repeticiones')
plt.subplot(1,2,2)
plt.hist(symbolsQ,label=label)
plt.legend()
plt.xlabel('Simbolos')
plt.ylabel('Repeticiones')
plt.show()
#/////////////////////////////////


#Grafia de simbolos transmitidos

zsymbI = np.array(PRI_List_to_FIR)
zsymbQ = np.array(PRQ_List_to_FIR)

plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(zsymbI,'o')
plt.xlim(0,20)
plt.grid(True)
plt.subplot(2,1,2)
plt.plot(zsymbQ,'o')
plt.xlim(0,20)
plt.grid(True)
plt.show()
#//////////////////////////////////


#Grafica de respuesta a la convolucion
symb_out0I = np.convolve(rc0,zsymbI,'full'); symb_out0Q = np.convolve(rc0,zsymbQ,'full')


plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.plot(symb_out0I,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(symb_out0Q,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%beta)
plt.xlim(1000,1250)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.figure(figsize=[10,6])
plt.plot(np.correlate(symbolsI,2*(symb_out0I[1:len(symb_out0I):int(os)]>0.0)-1,'same'))
plt.show()
#////////////////////////////////////////

#Grafica de diagrama ojo
fun.eyediagram(symb_out0I[100:len(symb_out0I)-100],os,5,Nbauds)
fun.eyediagram(symb_out0Q[100:len(symb_out0Q)-100],os,5,Nbauds)
#///////////////////////////


#Grafica de constelacion 
offset = 8
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


