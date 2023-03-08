#Ejemplo con matrices en Python Papi
import numpy as np

def Matriz(N,M):

    matriz = []
    for i in range (N):
        matriz.append([])
        for j in range (M):
            valor = float(input("Fila {} Columna {} :".format(i+1, j+1)))
            matriz [i].append(valor)
    print()

    """for N in matriz:
        print("[",end =" ")
        for element in N:
            print("{:8.2f}".format(element), end=" ")
        print("]")

    print()""" 
    return matriz
    
N = int(input("Ingresa cantidad de Filas: "))
M = int(input("Ingresa cantidad de Columnas: "))
print()
print("Vamos con la primera matriz \n")
a=np.matrix(Matriz(N,M))
print("Matriz (1): \n",np.matrix(a))
print()
print("Vamos con la segunda matriz \n")
b=np.matrix(Matriz(M,N))
print("Matriz (2): \n",np.matrix(b))
print()
print("EL producto punto de las matrices es: \n",np.dot(a,b))


