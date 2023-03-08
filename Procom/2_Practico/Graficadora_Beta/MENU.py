import numpy as np
import COMPRUEBA as Cm      #importamos librerias, y cabeceras creadas
import ERROR as Er
import DATA_PLOT as dp
import FIGPLOT as fp
#  ____________________________________________________________________________
# |Funcion: menu() menu principal que es el encaergado de la toma de los datos |
# |         y direccionamiento de los mismos a otras funciones                 |
# |Recibe: nada                                                                | 
# |retorna: nada                                                               | 
# |____________________________________________________________________________|

def menu(): #Menu principal para la toma de datos

    fila = int(input("Ingrese cantidad de filas: "))
    columna = int(input("Ingrese cantidad de columna: "))
    matriz = np.arange(1,((fila*columna)+1)).reshape(fila,columna)
    print("Su Area de trabajo sera una matriz de {}x{}".format(fila,columna))
    print("la cantidad de graficos individuales permitidos son: ({})".format(fila*columna))
    print("*"*50)
    print("Forma de la matriz:")
    print(matriz)
    print("*"*50)
    print("Ahora debe indicar la manera en la que se van a agrupar los graficos, recordar que solo se puede agrupar por filas.")
    print("Vea el siguiente ejemplo: (1,3),4,(5,6),(7,9) donde (1,3) tomamos valores desde 1 hasta 3")
    print()

    JoinVector  = eval(input("Ingrese las agrupaciones: ")) 
    warning = Cm.Comprueba(fila,columna,matriz,JoinVector) #Compruebo si el JoinVector fue ingresado de manera correcta
    while(warning!=0):
        Er.Error(warning)   #En caso de error se muestra un mensaje en la pantalla con el tipo de error
        JoinVector  = eval(input("Ingrese las agrupaciones: ")) #vuelve a preguntar hasta que el vector este correctamente ingresado
        warning = Cm.Comprueba(fila,columna,matriz,JoinVector)     

    #Una vez teniendo correctamente el JoinVector continuamos con los demas datos
    Max_SubPlot = len(JoinVector)
    print("*"*80)
    print("JoinVector correcto¡ la cantidad de SubPlot que puede hacer son: [{}]".format(Max_SubPlot))
    print("*"*80)
    print("Los Siguientes datos de los {} plot se deben ingresar c/u separado por una ','".format(Max_SubPlot))
    print("Por Ejemplo: plot,plot,stem,stem o 1,2,2,1, etc")
    print("*"*80)

    x,y0,numplot,show,typeGraf,xlim,ylim,xlabel,ylabel = dp.data_plot(Max_SubPlot) #De data_plot() obtengo los demas valores para figplot()

    fp.figplot(x, y0, fila, columna, JoinVector, numplot, show, typeGraf, xlim, ylim, xlabel, ylabel) #Funcion encargada de imprimir nuestra matriz de graficas
    #fin de menu()
