# Mensaje dinámico
import os
import time 
 
if os.name == "posix":
   var = "clear"       
elif os.name == "ce" or os.name == "nt" or os.name == "dos":
   var = "cls"
 
time.sleep(2)
 
os.system(var) 
print("****************************************") 
print("*                                      *")
print("*  ¡Bienvenidos a AprenderPython.net!  *")
print("*                                      *")
print("****************************************")
 
time.sleep(2)
os.system(var)
 
print("****************************************")
print("*                                      *")
print("*Aquí aprenderas a programar con Python*")
print("*                                      *")
print("****************************************")
 
time.sleep(2)
os.system(var)
 
print("****************************************")
print("*                                      *")
print("*         Es totalmente gratis         *")
print("*                                      *")
print("****************************************")
 
time.sleep(2)