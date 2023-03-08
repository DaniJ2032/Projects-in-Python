#|______________________________Graficadora 1.0b____________________________________|
#| Se toma los datos almacenados a la salida del filtro ya sea pre rotado o pos     |
#| tambien se puede graficar el diagrama de constelacion con los datos recibidios   |
#| ya sea constelacion normal o con una rotacion dada                               |
#|__________________________________________________________________________________|

import csv
import matplotlib.pyplot as plt 

#___Variables___#
offset      = 2 #Offset para diagrama de constelacion
offsetRot   = 1
os          = 4 #Over sampling del sistema

# archivoI        = '/home/danielito/Escritorio/Datos/Normal/DatosFiltroI.csv'     # PATH de archivos 
# archivoQ        = '/home/danielito/Escritorio/Datos/Normal/DatosFiltroQ.csv'     # enviados desde la fpga    
archivoRotadoI  = '/home/danielito/Escritorio/Datos/Rotados/11-DatosFiltroRotadoI.csv'
archivoRotadoQ  = '/home/danielito/Escritorio/Datos/Rotados/11-DatosFiltroRotadoQ.csv'


#___Se Extre los valores obtenidos de los filtros___#
# with open (archivoI) as f:

#     lecturaI = csv.reader(f)
#     valoresI = ''
#     valListI = []

#     for i in lecturaI:
#         valor_entero = i
#         valoresI = valor_entero 
#     for i in range (len (valoresI)-1):
#         valListI.append(float(valoresI[i])) 

# with open (archivoQ) as f:

#     lecturaQ = csv.reader(f)
#     valoresQ = ''
#     valListQ = []

#     for i in lecturaQ:
#         valor_entero = i
#         valoresQ = valor_entero 
#     for i in range (len (valoresQ)-1):
#         valListQ.append(float(valoresQ[i]))


with open (archivoRotadoI) as f:

    lecturaRotadaI = csv.reader(f)
    valoresI = ''
    valListRotadaI = []

    for i in lecturaRotadaI:
        valor_entero = i
        valoresI = valor_entero 
    for i in range (len (valoresI)-1):
        valListRotadaI.append(float(valoresI[i]))

with open (archivoRotadoQ) as f:

    lecturaRotadaQ = csv.reader(f)
    valoresQ = ''
    valListRotadaQ = []

    for i in lecturaRotadaQ:
        valor_entero = i
        valoresQ = valor_entero 
    for i in range (len (valoresQ)-1):
        valListRotadaQ.append(float(valoresQ[i]))


#__Grafia de respuesta del filtro pre rotado___#
# plt.figure(figsize=[10,6])
# plt.subplot(2,1,1)
# plt.title('Signal Filter I')
# plt.plot(valListI,'r-',linewidth=2.0)
# plt.xlim(0,450)
# plt.grid(True)

# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')

# plt.subplot(2,1,2)
# plt.title('Signal Filter Q')
# plt.plot(valListQ,'r-',linewidth=2.0)
# plt.xlim(0,450)
# plt.grid(True)

# plt.xlabel('Muestras')
# plt.ylabel('Magnitud')

#___Grafica de la respuesta del filtro post Rotado___#
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.title('Signal Filter Rotated I')
plt.plot(valListRotadaI,'r-',linewidth=2.0)
plt.xlim(0,450)
plt.grid(True)

plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.title('Signal Filter Rotated Q')
plt.plot(valListRotadaQ,'r-',linewidth=2.0)
plt.xlim(0,450)
plt.grid(True)

plt.xlabel('Muestras')
plt.ylabel('Magnitud')
# plt.show()

 
#__Grafica de diagrama de constelacion sin rotacion__#   
# plt.figure(figsize=[6,6])
# plt.plot(valListQ[offset:len(valListQ)-offset: int(os)], 
#          valListI[offset:len(valListI)-offset: int(os)], '.',linewidth=2.0)
# plt.xlim((-2, 2))
# plt.ylim((-2, 2))
# plt.grid(True)
# plt.xlabel('Real')
# plt.ylabel('Imag')
# plt.title('Diagram Constellation')

#__Grafica de diagrama de constelacion con rotacion__#   
plt.figure(figsize=[6,6])
plt.plot(valListRotadaQ[offsetRot:len(valListRotadaQ)-offsetRot: int(os)], 
         valListRotadaI[offsetRot:len(valListRotadaI)-offsetRot: int(os)], '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.title('Diagram Constellation Rotated')
plt.show()


