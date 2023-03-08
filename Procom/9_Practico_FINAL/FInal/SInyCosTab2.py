# |_______________________SinyCosTab2____________________________________|
# | Con este scriptse genera 1/4 de la onda Seno y coseno para posterior |
# | Armado de las ondas completas mediante simulacion de multiplexores   |
# | y tambien para el armado de archivos .dat que seran usados en la     |
# | implementacion del RTL                                               |    
# |______________________________________________________________________|  

import numpy as np
import matplotlib.pyplot as plt
from tool._fixedInt import *

# VARIABLES
lista_Sin        = []
lista_Cos        = []
lista_Sin_mux    = []   # Listas
lista_Cos_mux    = []
lista_Sin_Cuanti = []
lista_Cos_Cuanti = []

N           = 1024                   # Numero de muestras
frec        = 1.0/((1.0/100.0e6)*N)  # Frecuencia en base al num de meustras para un Fsamp = 100Mhz

#___Generacion de 1/4 de onda de Sen y Cos___#
for t in range(N):
    valor = np.sin((np.pi/2.0)*frec*(t/100.0e6))
    lista_Sin.append(valor)
 
for t in range(N):
    valor = np.cos((np.pi/2.0)*frec*(t/100.0e6))
    lista_Cos.append(valor)

#___Cuantificacion de los Valores____#
lista_Sin = list(lista_Sin)
lista_Cos = list(lista_Cos)

lista_Sin = arrayFixedInt(8, 6, lista_Sin, signedMode='S', roundMode='round', saturateMode='saturate')
lista_Cos = arrayFixedInt(8, 6, lista_Cos, signedMode='S', roundMode='round', saturateMode='saturate')

for ptr in range(len(lista_Sin)):
    lista_Sin[ptr]       = lista_Sin[ptr].fValue
    lista_Cos[ptr]       = lista_Cos[ptr].fValue

#___Creacion de archivo .dat para RTL___#
archivo = open('CuartoSin.dat', '+w') #con +w si no existe el archivo se lo crea

for i in range(len(lista_Sin)):

    valSin = hex(int(lista_Sin[i]*(2**6)))
    
    if (len(valSin) > 3): archivo.write(valSin)
    elif(len(valSin) == 3):
        valSin = hex(int(lista_Sin[i]*(2**6))).split('0x')[1]    
        valSin = valSin.zfill(2)        
        archivo.write('0x' + valSin)

    archivo.write('\n')
    
print("Writing complete Sin")
archivo.close()

print()
print()
archivo = open('CuartoCos.dat', '+w') #con +w si no existe el archivo se lo crea
for i in range(len(lista_Cos)):

    valCos = hex(int(lista_Cos[i]*(2**6)))

    if (len(valCos) > 3): archivo.write(valCos)
    elif(len(valCos) == 3):
        valCos = hex(int(lista_Cos[i]*(2**6))).split('0x')[1]    
        valCos = valCos.zfill(2)        
        archivo.write('0x' + valCos)

    archivo.write('\n')

print("Writing complete Cos")
print()
archivo.close()



