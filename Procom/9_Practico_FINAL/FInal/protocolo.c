/************************Trabajo Practico Integrador******************************
 * Sistema embebido para micro blazer de FPGA. 
 * con este archivo en c lo que se hace es tomar lo resivido por
 * el puerto serie enviado por la FPGA y desarmar la trama recibidia 
 * con el fin de realizar la opcion que fue ejegida.
 * Explicacion de la trama recibida:
 * 									El sistema esta implementado para
 * recibir una trama como la siguiente: 0x04800001 la cual posee
 * un ancho de 32bits, 8bytes, el cual se conforma de la siguiente  
 * manera.
 * 		  0x04 Bits [31:24] --> Opcion a ejecutar en el RF.  		
 * 	      0x80 Bits [23]    --> Enable propio del sistema para el RF.
 *        0X00 Bits [22:0]  --> Bytes libres para uso de alguna modificacion.
 * 		  0x01 Bits [22:0]  --> Sub opcion propia de la opcion principal.
 * A manera de asegurarse una estabilidad en la escritura del RF
 * se realiza una "triple escritura" de la siguiente manera.
 * 0x04800001 --> Enable en ON  = 0x80	
 * 0x04000001 --> Enable en OFF = 0x00
 * 0x04800001 --> Enable en ON  = 0x80
 * 	
 * Autores: Juarez Daniel, JOse Gomez Lazarte
 * Año:	2023
 ******************************************************************************/

//Librerias
#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xuartlite.h"
#include "microblaze_sleep.h"
#include <xil_printf.h>

//Definiciones
#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
//Device_ID Operaciones
#define def_SOFT_RST            0
#define def_ENABLE_MODULES      1
#define def_LOG_RUN             2
#define def_LOG_READ            3
#define	N						900	//Cantidad de datos de los filtros a enviar

//Variables
XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
XUartLite uart_module;

/*
*****************************************************************
* Funcion void TramaErr (char, char), la misma se encarga de
* enviar un mensaje de error si la trama que se recibio no cumple
* con los parametros
* RECIBE:
*		 dato1 y dato2 -> usado para armar la trama de error
* RETORNA:
*	      nada
*****************************************************************
*/
void TramaErr (char, char); 

//Funcion principal main()
int main(){

	init_platform();	//Inicio de perifericos en la FPGA

	/*Variables*/
	int Status         ;
	int indice      = 0;
	int error       = 0;
	int contador_BE = 0;
	unsigned char dato[4];

	u32  byte_dato_3   ;	//Variables para la trama recibida
	u32  byte_dato_2   ;
	u32  byte_dato_1   ;
	u32  byte_dato_0   ;
	u32  Error_bits [8];
	u32  resultado_dato;
	u32  value         ;
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
		read(stdin,&dato[0],1);	//Lectura de puerto serie

		switch (indice){
		case 0:
			if (dato[0] == 0xA4) break;
			else error = 1; // Se toma el dato si es erroneo entonces error = 1
			break;			// y se envia un mensaje de error al python

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
				byte_dato_3 = dato[0];	// Bytes de datos de la trama para la FPGA 
				break;

		case 5:
				byte_dato_2 = dato[0];
				break;

		case 6:
				byte_dato_1 = dato[0];
				break;

		case 7:
				byte_dato_0 = dato[0];
				break;

		case 8:									//Una vez obtenido todos los datos los concatenamos todos
			if (dato[0] == 0x44 && error == 0){	
				resultado_dato = (byte_dato_3 << 24) + (byte_dato_2 << 16) + (byte_dato_1 << 8) + byte_dato_0;

				//Escritura en el gpo0 para el modulo de RF de la FPGA
				if(resultado_dato != 0x06800000 || 0x04800001){
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (resultado_dato & (0xFF7FFFFF)));
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) resultado_dato);	
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (resultado_dato & (0xFF7FFFFF)));
				}

				if(resultado_dato == 0x00800000){	//Reset 
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x00800001 & (0xFF7FFFFF)));
					XGpio_DiscreteWrite(&GpioOutput,1, (u32)  0x00800001                );
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x00800001 & (0xFF7FFFFF)));
				}

				if(resultado_dato == 0x06800000){	//Lectura y envio de Bits y errores transmitidos

					while (contador_BE < 8){
						XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x06000000 | (contador_BE & 0x0000000F)));
						XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x06800000 | (contador_BE & 0x0000000F)));
			        	XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x06000000 | (contador_BE & 0x0000000F)));
						Error_bits[contador_BE] = XGpio_DiscreteRead(&GpioInput, 1);

						unsigned char trama_EB [] = {0xA4, 0x00, 0x00, 0x01, (Error_bits[contador_BE] & 0xFF), ((Error_bits[contador_BE]>>8) & 0xFF), ((Error_bits[contador_BE]>>16) & 0xFF), ((Error_bits[contador_BE]>>24) & 0xFF), 0x44};
						while(XUartLite_IsSending(&uart_module)){};
						XUartLite_Send(&uart_module,trama_EB,9);
						contador_BE += 1;
					}
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x05800000 & (0xFF7FFFFF)));
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x05800000);
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x05800000 & (0xFF7FFFFF)));
				}


 				if(resultado_dato == 0x04800001){	//Lectura de datos logeados en la RAM

 					for (int j = 0; j < N; j ++ ){

						XGpio_DiscreteWrite(&GpioOutput,1, (u32) ((0x04810000 | (j & 0x0000FFFF)) & (0xFF7FFFFF)));
						XGpio_DiscreteWrite(&GpioOutput,1, (u32)  0x04810000  | (j & 0x0000FFFF)) ;
						XGpio_DiscreteWrite(&GpioOutput,1, (u32) ((0x04810000 | (j & 0x0000FFFF)) & (0xFF7FFFFF)));

 						value = XGpio_DiscreteRead(&GpioInput, 1);

 						unsigned char trama_filtro [] = {0xA4, 0x00, 0x00, 0x01, (value & 0xFF), ((value>>8) & 0xFF), ((value>>16) & 0xFF), ((value>>24) & 0xFF), 0x44};

						while(XUartLite_IsSending(&uart_module)){};
						XUartLite_Send(&uart_module,trama_filtro,9);
 					}

					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x04800000 & (0xFF7FFFFF)));
					XGpio_DiscreteWrite(&GpioOutput,1, (u32)  0x04800000);
					XGpio_DiscreteWrite(&GpioOutput,1, (u32) (0x04800000 & (0xFF7FFFFF)));
 				}
				break;
			}//if (dato[0] == 0x44 && error == 0)
			else{
				TramaErr('0','F'); // Datos para armado de trama de error 
				break;
			}
		} //fin del case
		indice += 1; //indice para el case

		if (indice == 9 ){
			indice 		= 0;
			error 		= 0; 
			contador_BE = 0;
		}
	}  //Fin de while(1)
	cleanup_platform();
	return 0;
} //Fin de main()

// Funcion para envio de trama tras un error
void TramaErr (char dato1, char dato2){
    unsigned char trama [7] = {0xA4, 0x00, 0x00, 0x01, dato1, dato2, 0x44};
    while(XUartLite_IsSending(&uart_module)){};
	XUartLite_Send(&uart_module,trama,7);
}











