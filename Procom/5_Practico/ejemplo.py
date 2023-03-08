#__________Uso de la libreria fixendInt para punto flotante___________#
import math
import numpy as np
from tool._fixedInt import *

"""Definicion de los objetos de la clase DeFixedInt. Atentos a la nueva definicion
Ejemplo: DeFix_object=DeFixedInt(intWidth=15, fractWidth=15, signedMode = 'S', roundMode='trunc', saturateMode='saturate')

-->intWidth=Numero Entero Positivo. Cantidad de bits totales de la palabra. Por defecto 0
-->fractWidth=Numero Entero Positivo. Cantidad de bits fraccionales de la palabra. Por defecto 15
-->signedMode= 'S' (signado) o 'U' (no signado). Por defecto 'S'
-->roundMode= 'trunc' (truncado) o 'round' (redondeo). Ajuste de resolucion. Por defecto 'trunc'
-->satureMode= 'saturate' (saturado) o 'wrap' (overflow). Ajuste de rango. Por defecto 'saturate'

Nota: Noten que ya no se define mas value=0 o como se ponia antes DeFix_object=DeFixedInt(4,2,0,'trunc','saturate)  
"""
#Creamos un Objeto fixedInt

#Modo de creacion completa (teniendo en cuenta todos los parámetros)
#En eset caso truncado con saturacion S(8,7)
num_1=DeFixedInt(roundMode='trunc',signedMode = 'S',intWidth=7,fractWidth=4,saturateMode='saturate')
#=====================================

#Ahora asignamos un valor a nuestrop objeto num_1

num_1.value = 6.8758 #Cargo el valor flotante a fixear al objeto a
print()
print ("Pepito: ",num_1.fValue)
print ("\nPara a: ")
print ('Float: %f|'%num_1.fValue,'NBI: %d|'%num_1.intWidth,'NBF: %d|'%num_1.fractWidth,'NB: %d|'%num_1.width)
print ("\nEntero Equivalente")
print ('Int: %d|'%num_1.intvalue,'Bin: ',bin(num_1.intvalue))
print ("\n----> Rango de a: "); 
num_1.showRange()
print()
#num_1.showValueRange() #MUestra todos los valores del rango
