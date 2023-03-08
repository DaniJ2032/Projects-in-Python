import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

os             = 4
beta           = 0.5
Nsymb          = 511        # Numero de simbolos
T              = 1.0/100e6 # Periodo de baudio
Ts             = T/os       # Frecuencia de muestreo
Nfreqs         = 256        # Cantidad de frecuencias
Nbauds         = 6.0        # Cantidad de baudios del filtro
PRBSI          = np.array ([1,1,0,1,0,1,0,1,0])
PRBSQ          = np.array ([1,1,1,1,1,1,1,1,0])
SR1            = np.array ([0,0,0,0,0,0])
SR2            = np.array ([0,0,0,0,0,0])
coeficientes   = np.array ([ 8.95103186e-34,  4.77279499e-03,  1.71488822e-02,  2.27496429e-02,
                            -1.54351892e-16, -5.76127319e-02, -1.20042175e-01, -1.22501738e-01,
                             1.60734027e-15,  2.62503724e-01,  6.00210877e-01,  8.87236072e-01,
                             1.00000000e+00,  8.87236072e-01,  6.00210877e-01,  2.62503724e-01,
                            -2.94478863e-15, -1.22501738e-01, -1.20042175e-01, -5.76127319e-02,
                             7.40915352e-16,  2.27496429e-02,  1.71488822e-02,  4.77279499e-03] )

coeficientes = arrayFixedInt(8, 6, coeficientes, signedMode='S', roundMode='round', saturateMode='saturate')
for ptr in range(len(coeficientes)):
    coeficientes[ptr] = coeficientes[ptr].fValue
coeficientes = coeficientes.tolist()   

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

for j in range(1):
    for i in range(511):
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
        
        for i in range(os - 1):
            salidaPRBSI.append(0)    #Sobremuestreo
            salidaPRBSQ.append(0)
        
        SR1    = np.roll(SR1,1)
        SR1[0] = SalidaPRBSI_actual
        SR2    = np.roll(SR2,1)
        SR2[0] = SalidaPRBSQ_actual
        
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
            symb_out0I.append(aux_symb_outI)
            symb_out0Q.append(aux_symb_outQ)
            
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
                

    acumulador_arregloI.append(contador_berI)
    if (contador_berI == 0):
        print("Latencia minima en I:",j) 
    
    acumulador_arregloQ.append(contador_berQ)
    if (contador_berQ == 0):
        print("Latencia minima en Q:",j)
           
    #Reseteo de elementos
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
       
symb_out0Q       = arrayFixedInt(8, 6, symb_out0Q, signedMode='S', roundMode='round', saturateMode='saturate')
symb_out0I       = arrayFixedInt(8, 6, symb_out0I, signedMode='S', roundMode='round', saturateMode='saturate')
symb_out0Q_sinOS = arrayFixedInt(8, 6, symb_out0Q_sinOS, signedMode='S', roundMode='round', saturateMode='saturate')
symb_out0I_sinOS = arrayFixedInt(8, 6, symb_out0I_sinOS, signedMode='S', roundMode='round', saturateMode='saturate')


noiseI = (np.random.uniform(0, 0.1, np.size(symb_out0I)))    #Generacion de ruido
noiseQ = (np.random.uniform(0, 0.1, np.size(symb_out0I)))

for ptr in range(len(symb_out0Q)):
    symb_out0Q[ptr]       = symb_out0Q[ptr].fValue
    symb_out0I[ptr]       = symb_out0I[ptr].fValue

symb_out0Q = symb_out0Q + noiseQ
symb_out0I = symb_out0I + noiseI #Ruido montado


for ptr in range(len(symb_out0Q_sinOS)):    
    symb_out0Q_sinOS[ptr] = symb_out0Q_sinOS[ptr].fValue 
    symb_out0I_sinOS[ptr] = symb_out0I_sinOS[ptr].fValue     



Xrvec   = []
Xivec   = []
N       =  (45*np.pi)/180 
print(len(symb_out0Q))
print(len(symb_out0I))
####FUNCIONA? ROTACION DE SIMBOLOS......
for i in range (len(symb_out0Q)):
    Xrvec.append((symb_out0I[i] * np.sin((N)) +  symb_out0Q[i] * np.cos((N))))
    Xivec.append((symb_out0I[i] * np.cos((N)) -  symb_out0Q[i] * np.sin((N))))    
###############################################################
Xrvec             = np.array(Xrvec)
Xivec             = np.array(Xivec)


salidaPRBSI       = np.array(salidaPRBSI      )
salidaPRBSQ       = np.array(salidaPRBSQ      )
salidaPRBSI_sinOS = np.array(salidaPRBSI_sinOS)
salidaPRBSQ_sinOS = np.array(salidaPRBSQ_sinOS)
PRBSI_AUX         = np.array(PRBSI_AUX        )
PRBSQ_AUX         = np.array(PRBSQ_AUX        )
symb_out0Q        = np.array(symb_out0Q       )
symb_out0I        = np.array(symb_out0I       )
symb_out0I_sinOS  = np.array(symb_out0I_sinOS )
symb_out0Q_sinOS  = np.array(symb_out0Q_sinOS )



# ###################################################### Grafica de simbolos
# label = 'Simbolos: %d' % Nsymb
# plt.figure(figsize=[14,6])
# plt.subplot(1,2,1)
# plt.hist(PRBSI_AUX,label=label)
# plt.legend()
# plt.xlabel('Simbolos')
# plt.ylabel('Repeticiones')
# plt.subplot(1,2,2)
# plt.hist(PRBSQ_AUX,label=label)
# plt.legend()
# plt.xlabel('Simbolos')
# plt.ylabel('Repeticiones')

# plt.show()
# ###########################################################################    
# plt.figure(figsize=[10,6])
# plt.subplot(2,1,1)
# plt.plot(salidaPRBSI,'o')
# plt.xlim(0,20)
# plt.grid(True)
# plt.subplot(2,1,2)
# plt.plot(salidaPRBSQ,'o')
# plt.xlim(0,20)
# plt.grid(True)
# plt.show()
# ############################################################################

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

# ###########################################################################
# plt.figure()
# for ptr in range(len(salidaPRBSI_sinOS)):
#     if (salidaPRBSI_sinOS[ptr] == 0):
#         salidaPRBSI_sinOS[ptr] = 1
#     else:
#         salidaPRBSI_sinOS[ptr] = -1 
# plt.plot(np.correlate(symb_out0I_sinOS,salidaPRBSI_sinOS,'same'))
# plt.show()

# ###########################################################################

# def resp_freq(filt, Ts, Nfreqs):
#     """Computo de la respuesta en frecuencia de cualquier filtro FIR"""
#     H = [] # Lista de salida de la magnitud
#     A = [] # Lista de salida de la fase
#     filt_len = len(filt)

#     #### Genero el vector de frecuencias
#     freqs = np.matrix(np.linspace(0,1.0/(2.0*Ts),Nfreqs))
#     #### Calculo cuantas muestras necesito para 20 ciclo de
#     #### la mas baja frec diferente de cero
#     Lseq = 20.0/(freqs[0,1]*Ts)

#     #### Genero el vector tiempo
#     t = np.matrix(np.arange(0,Lseq))*Ts

#     #### Genero la matriz de 2pifTn
#     Omega = 2.0j*np.pi*(t.transpose()*freqs)

#     #### Valuacion de la exponencial compleja en todo el
#     #### rango de frecuencias
#     fin = np.exp(Omega)

#     #### Suma de convolucion con cada una de las exponenciales complejas
#     for i in range(0,np.size(fin,1)):
#         fout = np.convolve(np.squeeze(np.array(fin[:,i].transpose())),filt)
#         mfout = abs(fout[filt_len:len(fout)-filt_len])
#         afout = np.angle(fout[filt_len:len(fout)-filt_len])
#         H.append(mfout.sum()/len(mfout))
#         A.append(afout.sum()/len(afout))

#     return [H,A,list(np.squeeze(np.array(freqs)))]


# ### Calculo respuesta en frec para el pulso
# [H0,A0,F0] = resp_freq(coeficientes, Ts, Nfreqs)

# ### Generacion de los graficos
# plt.figure(figsize=[14,6])
# plt.semilogx(F0, 20*np.log10(H0),'r', linewidth=2.0, label=r'$\beta=0.0$')

# plt.axvline(x=(1./Ts)/2.,color='k',linewidth=2.0)
# plt.axvline(x=(1./T)/2.,color='k',linewidth=2.0)
# plt.axhline(y=20*np.log10(0.5),color='k',linewidth=2.0)
# plt.legend(loc=3)
# plt.grid(True)
# plt.xlim(F0[1],F0[len(F0)-1])
# plt.xlabel('Frequencia [Hz]')
# plt.ylabel('Magnitud [dB]')
# plt.show()
# ############################################################################################

# def eyediagram(data, n, offset, period):
#     span     = 2*n
#     segments = int(len(data)/span)
#     xmax     = (n-1)*period
#     xmin     = -(n-1)*period
#     x        = list(np.arange(-n,n,)*period)
#     xoff     = offset

#     plt.figure()
#     for i in range(0,segments-1):
#         plt.plot(x, data[(i*span+xoff):((i+1)*span+xoff)],'b')       
#     plt.grid(True)
#     plt.xlim(xmin, xmax)
#     plt.show()

# eyediagram(symb_out0I[100:len(symb_out0I)-100],os,5,Nbauds)
# eyediagram(symb_out0Q[100:len(symb_out0Q)-100],os,5,Nbauds)
# plt.show()
# ##############################################################################################

offset = 8

plt.figure(figsize=[6,6])
plt.plot(Xrvec[100+offset:len(symb_out0I)-(100-offset):int(os)],
         Xivec[100+offset:len(symb_out0Q)-(100-offset):int(os)],
             '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.show()
##############################################################################################