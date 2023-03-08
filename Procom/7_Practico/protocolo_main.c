/*******Trabajo Practico N 7 Manejo de puerto Serie de FPGA************
 *
 * Se toma la trama enviada por el script de python "uart7.py", se la
 * decodifica y en base a la informacion enviada se prenden led's con
 * diferentes colores o se envia el estado de los switch de la placa.
 * tambien si se detecta un error en la trama enviada este programa
 * envia una "F" indicando error en trama recibida
 *
 * */

#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xuartlite.h"
#include "microblaze_sleep.h"

#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID

//Device_ID Operaciones
#define def_SOFT_RST            0
#define def_ENABLE_MODULES      1
#define def_LOG_RUN             2
#define def_LOG_READ            3

XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;

void EnvioTrama (char, char);


int main(){

	init_platform();

	/*Variables*/
	int Status;
	int indice = 0;
	int error  = 0;
	int flag_inicio = 0;
	unsigned char dato[4];
	unsigned char salida;

	u32  value;
	u32  byte_dato_low;
	u32  byte_dato_high;
	u32  resultado_dato;
	/*******************/

	/*Inicializacion de puertos*/
	XUartLite_Initialize(&uart_module, 0);
	GPO_Value=0x00000000;
	GPO_Param=0x00000000;

	Status=XGpio_Initialize(&GpioInput, PORT_IN);
	if(Status!=XST_SUCCESS){
		return XST_FAILURE;
	}
	Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
	if(Status!=XST_SUCCESS){
		return XST_FAILURE;
	}
	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);
	/***************************************************/
	/*Bucle*/
	while(1){
		read(stdin,&dato[0],1);	//Leo el puerto serie

		switch (indice){
		case 0:
			if (dato[0] == 0xA2) break;	//tomo el dato si es erroneo error = 1
			else error = 1;
			break;

		case 1:
			if (dato[0] == 0x00 && error == 0) break;
			else error = 1;
			break;

		case 2:
			if (dato[0] == 0x00 && error == 0) break;
			else error = 1;
			break;

		case 3:
			if (dato[0] == 0x01 && error == 0) break;
			else error = 1;
			break;

		case 4:
				byte_dato_high = dato[0];
				break;

		case 5:
				byte_dato_low = dato[0];
				break;

		case 6:
			if (dato[0] == 0x42 && error == 0){

			resultado_dato = (byte_dato_high << 8) + byte_dato_low; 	//Se arma el valor para los led's
			XGpio_DiscreteWrite(&GpioOutput,1, (u32) resultado_dato);	//Se escribe resultado en los led's

			if(resultado_dato == 0x001){	//Pido el estado de los switch
				XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
				value = XGpio_DiscreteRead(&GpioInput, 1);
				salida=(char)(value&(0x0000000F));	//Se enmascara el valor
				EnvioTrama('S',salida);				//Se envia el valor de los Switch
				resultado_dato = 0x000;
			}

			}else EnvioTrama('0','F');	//Se envia el mensaje de error
			break;

		} //fin del case

        /**********************************/
		if (flag_inicio == 0 ) indice += 1; //Se incrementa el indice para recorrer el case

		if 	(indice == 7 ){
			indice 		= 0;
			flag_inicio	= 0;	//cuando el indice es 7 lo reinicio hasta la proxima
			error 		= 0;	//trama a recibir
		}
		/**********************************/

	} //Fin de while(1)
	cleanup_platform();
	return 0;
} //Fin de main()

/*
 *
 * */

/*Con esta funcion se envia una trama ya sea con el valor de los switch
 * o cuando se detecto un error*/

void EnvioTrama (char dato1, char dato2){

    unsigned char trama [7] = {0xA2, 0x00, 0x00, 0x01, dato1, dato2, 0x42};
    while(XUartLite_IsSending(&uart_module)){};
	XUartLite_Send(&uart_module,trama,7);
}

