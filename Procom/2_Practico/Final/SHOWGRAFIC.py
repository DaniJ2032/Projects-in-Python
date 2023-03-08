import numpy as np
#  ____________________________________________________________________________________________________________
# |Funcion: show_grafic() toma todos los valores de figplot y verifica en vase al vector show[] cuales datos de|
# |         los subplot no se imprimiran en la matriz de graficos debido a que se ingreso un "false".          | 
# |         Ademas tomamos todos los parametros del los plot que se les dio "true" para imprimirlos            |
# |Recibe: Los parametros para realizar los multiples SubPlot                                                  | 
# |retorna: los parametros de los subplot que corresponden a show="true"                                       | 
# |____________________________________________________________________________________________________________|

def show_grafic(x, y0, filas, columnas, JoinVector, numplot, show, typeGraf, xlim, ylim, xlabel, ylabel):

    Colum_Init  = [1]
    x2 = [] 
    y2 = []
    JoinVector2 = []    #Nuevos Vectores de datos 
    numplot2 = []
    typeGraf2 = []
    xlim2 = [] 
    ylim2 = [] 
    xlabel2 = []
    ylabel2 = []

    matriz = np.arange(1,((filas*columnas)+1)).reshape(filas,columnas)
    
    for i in range (columnas):               
        if i == 0:
            Colum_Init= [fila[i] for fila in matriz]

    for i in range (len(JoinVector)):
        if show[i] == 'true' : 
            x2.append(x[i])
            y2.append(y0[i])    
            JoinVector2.append(JoinVector[i])  #almacenos los datos en los nuevos vectores 
            numplot2.append(numplot[i])
            typeGraf2.append(typeGraf[i])
            xlim2.append(xlim[i]) 
            ylim2.append(ylim[i])
            xlabel2.append(xlabel[i])
            ylabel2.append(ylabel[i]) 
        if show[i] == 'false': 
            continue
    return x2,y2,JoinVector2,numplot2,typeGraf2,xlim2,ylim2,xlabel2,ylabel2,Colum_Init #retorno de los valores finales        
    #fin de la funcion show_grafic()