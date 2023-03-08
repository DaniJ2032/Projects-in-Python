#________________TP_N_6 Punto 1: Simulador en punto flotante__________________#
import numpy as np
import matplotlib.pyplot as plt
import Funtion as fun
from tool._fixedInt import *   #Libreria para el uso de punto fijo


#___________Parametros generales______________#
T     = 1.0/21.0e9  # Periodo de baudio
Nsymb = 1000        # Numero de simbolos
os    = 4           # Over Sampling

## Parametros de la respuesta en frecuencia
Nfreqs = 256        # Cantidad de frecuencias

## Parametros del filtro de caida cosenoidal
beta   = 0.5        # Roll-Off
Nbauds = 6.0        # Cantidad de baudios del filtro

## Parametros funcionales
Ts = T/os           # Frecuencia de muestreo
########################################################3


#Calculo de pulso para un roll off = 0.5
(t,rc0) = fun.rcosine(beta, T,os,Nbauds,Norm=False)
#Graficas para respuesta al impulso
print (np.sum(rc0**2))

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
symbolsI = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1
symbolsQ = 2*(np.random.uniform(-1,1,Nsymb)>0.0)-1

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
zsymbI = np.zeros(os*Nsymb); zsymbI[1:len(zsymbI):int(os)]=symbolsI
zsymbQ = np.zeros(os*Nsymb); zsymbQ[1:len(zsymbQ):int(os)]=symbolsQ

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
symb_out0I = np.convolve(rc0,zsymbI,'same'); symb_out0Q = np.convolve(rc0,zsymbQ,'same')

for i in range (10):
    print(symb_out0I[i])
print()
print()
for i in range (10):
    print(symb_out0Q[i])

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
plt.plot(np.correlate(symbolsI,2*(symb_out0I[3:len(symb_out0I):int(os)]>0.0)-1,'same'))
plt.show()
#////////////////////////////////////////


#Grafica de diagrama ojo
fun.eyediagram(symb_out0I[100:len(symb_out0I)-100],os,5,Nbauds)
fun.eyediagram(symb_out0Q[100:len(symb_out0Q)-100],os,5,Nbauds)
#///////////////////////////


#Grafica de constelacion 
offset = 6
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