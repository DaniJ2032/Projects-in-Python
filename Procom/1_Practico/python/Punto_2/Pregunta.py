import Menu_Principal as M

def Valuar(opc,opc2,opc3):
        
   while(opc>7):
        print()
        print("*"*45)
        print("Opcion incorrecta, escoja una opcion entre (1) Y (5)")
        print("*"*45,"\n")
        opc = 0
        M.Menu()

   while(opc2>5):
        print()
        print("*"*45)
        print("Opcion incorrecta, escoja una opcion entre (1) Y (4)")
        print("*"*45,"\n")
        opc2 = 0
        M.Menu2() 

   while(opc3>4):
        print()
        print("*"*45)
        print("Opcion incorrecta, escoja una opcion entre (1) Y (4)")
        print("*"*45,"\n")
        opc3 = 0
        M.MenuPunto()        

def Pregunta():
    resp = str(input("Desea vovler a realizar una operacion? (S)/(N): "))
    if(resp == 'S' or resp == 's'):
        M.Menu()
    elif(resp == 'N' or resp == 'n'): 
        print("Hasta Luego....\n")
        exit  


        