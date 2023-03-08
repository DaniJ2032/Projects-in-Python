#Ejemplo de vectores en Python Papi
import numpy as np

def Vector(M):

    vector = []
    for i in range(M):
        num = float(input("Elemento {}: ".format(i+1)))
        vector.append(num)
    print()
    return vector

M = int(input("Ingrese el tamaño de los vectores: "))

print("Vamos con el Primer Vector:\n")
a = Vector(M)
print("Vector (1): ",a)
print()
print("Vamos con el Segundo Vector:\n")
b = Vector(M)
print("Vector (2): ",b)
print("Producto Punto entre los vectores es:", np.dot(a,b))
print()
