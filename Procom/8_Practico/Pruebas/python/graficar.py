import csv
import matplotlib.pyplot as plt 

archivoI = '/home/danielito/Escritorio/DatosFiltroI.csv'
archivoQ = '/home/danielito/Escritorio/DatosFiltroQ.csv'

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

plt.figure(figsize=[25,20])
plt.subplot(2,1,1)
plt.plot(valListI,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%0.5)
plt.xlim(0,450)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.subplot(2,1,2)
plt.plot(valListQ,'r-',linewidth=2.0,label=r'$\beta=%2.2f$'%0.5)
plt.xlim(0,450)
plt.grid(True)
plt.legend()
plt.xlabel('Muestras')
plt.ylabel('Magnitud')

plt.show()
