import csv
import matplotlib.pyplot as plt 



# archivoConstelacionI    = '/home/danielito/Escritorio/DatosConstelacionRotadaI.csv'
# archivoConstelacionQ    = '/home/danielito/Escritorio/DatosConstelacionRotadaQ.csv'
# archivoI    = '/home/danielito/Escritorio/DatosConstelacionI.csv'
# archivoQ    = '/home/danielito/Escritorio/DatosConstelacionQ.csv'
archivoI    = '/home/danielito/Escritorio/DatosFiltroI.csv'
archivoQ    = '/home/danielito/Escritorio/DatosFiltroQ.csv'

offset      = 3
os          = 4

#___Se Extre los valores obtenidos de los filtros___#
with open (archivoI) as f:

    lecturaI = csv.reader(f)
    valoresI = ''
    valListI = []

    for i in lecturaI:
        valor_entero = i
        valoresI = valor_entero 
    for i in range (len (valoresI)-1):
        valListI.append(float(valoresI[i]))

with open (archivoQ) as f:

    lecturaQ = csv.reader(f)
    valoresQ = ''
    valListQ = []

    for i in lecturaQ:
        valor_entero = i
        valoresQ = valor_entero 
    for i in range (len (valoresQ)-1):
        valListQ.append(float(valoresQ[i]))

#___Se Extre los valores obtenidos de la constelacion___#
# with open (archivoConstelacionI) as f:

#     lecturaConstelacionI = csv.reader(f)
#     valoresI = ''
#     valListConstelacionI = []

#     for i in lecturaConstelacionI:
#         valor_entero = i
#         valoresI = valor_entero 
#     for i in range (len (valoresI)-1):
#         valListConstelacionI.append(float(valoresI[i]))
        
# with open (archivoConstelacionQ) as f:

#     lecturaConstelacionQ = csv.reader(f)
#     valoresQ = ''
#     valListConstelacionQ = []

#     for i in lecturaConstelacionQ:
#         valor_entero = i
#         valoresQ = valor_entero 
#     for i in range (len (valoresQ)-1):
#         valListConstelacionQ.append(float(valoresQ[i]))


#__Grafia de respuesta del Filtro__#
plt.figure(figsize=[10,6])
plt.subplot(2,1,1)
plt.title('Signal Filter I')
plt.plot(valListI,'r-',linewidth=2.0)
plt.xlim(0,450)
plt.grid(True)

plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.title('Signal Filter Q')
plt.plot(valListQ,'r-',linewidth=2.0)
plt.xlim(0,450)
plt.grid(True)

plt.xlabel('Muestras')
plt.ylabel('Magnitud')
  
#__Grafica de Diagrama de Constelacion__#   
# plt.figure(figsize=[6,6])
# plt.plot(valListConstelacionQ, valListConstelacionI, '.',linewidth=2.0)
# plt.xlim((-2, 2))
# plt.ylim((-2, 2))
# plt.grid(True)
# plt.xlabel('Real')
# plt.ylabel('Imag')
# plt.title('Diagram Constellation')
# plt.show()

plt.figure(figsize=[6,6])
plt.plot(valListQ[offset:len(valListQ)-offset: int(os)], valListI[offset:len(valListI)-offset: int(os)], '.',linewidth=2.0)
plt.xlim((-2, 2))
plt.ylim((-2, 2))
plt.grid(True)
plt.xlabel('Real')
plt.ylabel('Imag')
plt.title('Diagram Constellation')
plt.show()
