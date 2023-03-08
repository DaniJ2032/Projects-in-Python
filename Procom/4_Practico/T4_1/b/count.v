/*_____TP_4_Punto_B Agregamos un 3er barrido de leds______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module count
#(  parameter NB_SW = 3, NB_COUNTER = 32 ) 
(
    output  o_valid,            //Bit habilitante del contador
    input   [NB_SW - 1:0] i_sw, //Selector de los registros y enable del contador
    input   i_reset,            //Reset global
    input   clock               //Señal de clock
);

//Local Parameter (Variables Privadas)
localparam R0 = 2**(NB_COUNTER-11);
localparam R1 = 2**(NB_COUNTER-12);   //Limite de tiempo el cual los led estaran prendidos 
localparam R2 = 2**(NB_COUNTER-13);
localparam R3 = 2**(NB_COUNTER-14);

//conexiones y registros
wire    [NB_COUNTER-1 : 0]    limit_ref;    //Entradas de 32bits de los registros R0 --> R3 para el comparador
reg     [NB_COUNTER-1 : 0]   counter;       //Registro de contador
reg     valid;                              //Registro de validacion del contador


///Declaracion del comparador  
assign limit_ref = {i_sw[2:1] == 2'b00} ? R0 :  //Asigno el limite de referencia en el comparador
                   {i_sw[2:1] == 2'b01} ? R1 :
                   {i_sw[2:1] == 2'b10} ? R2 : R3;     


//Descripcion del contador
always @(posedge clock) begin 
    
    if(i_reset) begin   //si tenemos el reset activado 
        counter <={NB_COUNTER{1'b0}}; 
        valid <= 1'b0;                //Resetea el contador y el dato de validacion           
    end
    
    else if (i_sw[0]) begin  

    if(counter <= limit_ref) begin      //cuento hasta el limite_ref
       counter <= counter+1;            //incremeto el contador  
       valid <= 1'b0;                   //reseteo la salida de validacion del comparador para el shiftReg
    end    
    else begin 
        counter <={NB_COUNTER{1'b0}}; //resetea el contador
        valid <= 1'b1;                 //Habilito la salida de validacion para el shiftReg
    end
    
    end
    else begin 
        counter <= counter; 
        valid <= valid;     //no genero cambios hasta el prox pulso de relog
    end
end //fin de always()

//salida
assign o_valid = valid; //salida de validacion del contador     

endmodule



