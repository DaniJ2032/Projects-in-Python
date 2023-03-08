import os
import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import * 


#____Semillas para las PRBS_____
PRBSI       =   [0, 1, 0, 1, 0, 1, 0, 1, 1] # --> Semilla cargada 0x1AA
PRBSQ       =   [0, 1, 1, 1, 1, 1, 1, 1, 1] # --> Semilla cargada 0x1FE
Nsymb       =   511                         # --> 511 muestras
PRQ_List_to_FIR    =   []
PRQ_Out_to_Grafic  =   []

PRI_List_to_FIR    =   []
PRI_Out_to_Grafic  =   [] 
os                 =   4
#Coeficientes para el filtro
rc0 = np.array([8.95103186e-34,  4.77279499e-03,  1.71488822e-02,  2.27496429e-02, 
-1.54351892e-16, -5.76127319e-02, -1.20042175e-01, -1.22501738e-01, 
 1.60734027e-15,  2.62503724e-01,  6.00210877e-01,  8.87236072e-01,
 1.00000000e+00,  8.87236072e-01,  6.00210877e-01,  2.62503724e-01,
-2.94478863e-15, -1.22501738e-01, -1.20042175e-01, -5.76127319e-02,
 7.40915352e-16,  2.27496429e-02,  1.71488822e-02,  4.77279499e-03,])

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


#____Cauntificacion de los coeficientes____#
Cuantirc0 = arrayFixedInt(8, 7, rc0, signedMode='S', roundMode='trunc', saturateMode='saturate') #S (8,7) Trunc con saturacion

for i in range (len(rc0)):
    rc0aux.append(Cuantirc0[i].fValue)
rc0 = np.array(rc0aux)
#############################################

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

    countQ = 0 
    countI = 0



symb_out0Q  = np.array(Out_FIR_Q)
PRQ_Out_to_Grafic   = np.array(PRQ_Out_to_Grafic)   # --> obtengo el dato de salida Q
symbolsQ    = PRQ_Out_to_Grafic

symb_out0I  = np.array(Out_FIR_I)
PRI_Out_to_Grafic   = np.array(PRI_Out_to_Grafic)   # --> obtengo el dato de salida I
symbolsI = PRI_Out_to_Grafic  # Salidas de la PRBS para la grafica


#________________________Graficos_____________________________#

#Distribucion de simbolos
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

#Respuesta a la convolucion 
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
