/*MODULO CONTADOR*/

module count
#(  parameter NB_SW = 3, NB_COUNTER = 32 ) //Parametros (variables publicas)--> Son a nivel de modulo y bastante utilizado a nivel de modificacion de ancho de puertos
(
    output  o_valid,            //Bit habilitante del contador
    input   [NB_SW - 1:0] i_sw, //Selector de los registros y enable del contador
    input   i_reset,            //Reset global
    input   clock               //Señal de clock
);

//Local Parameter (Variables Privadas)
//Son parametros propios de un modulo, no pueden cambiar su vlor
localparam R0 = 2**(NB_COUNTER-11);
localparam R1 = 2**(NB_COUNTER-12);   //Limite de tiempo el cual los led estaran prendidos 
localparam R2 = 2**(NB_COUNTER-13);
localparam R3 = 2**(NB_COUNTER-14);

wire    [NB_COUNTER-1:0]    limit_ref;  //Entradas de 32bits de los registros R0 --> R3 para el comparador
reg     [NB_COUNTER-1 :0]   counter;  //Registro de contador
reg     valid;                      //registro de validacion del contador

/*Compare*/
/*Mux selector de los registros con sentencia ternaria*/  
assign limit_ref = {i_sw[2:1] == 2'b00} ? R0 :  //Asigno el limite de referencia en el comparador
                   {i_sw[2:1] == 2'b01} ? R1 :
                   {i_sw[2:1] == 2'b10} ? R2 : R3;     
///////////////////

/*Contador*/
always @(posedge clock) begin //begin :alwaysCounter //Etiqeuta
    
    if(i_reset) begin   //si tenemos el reset activado
     // count <= 32'b0000_0000_0000_0000_0000_0000_0000_0000; 
        counter <={NB_COUNTER{1'b0}}; //Metodo de repeticion de esta manera podemos resetear la variable de manera mas dinamica 
        valid <= 1'b0;                //reseteo la salida de validacion del comparador para el shiftReg           
    end
    else if (i_sw[0]) begin //si el i_sw[] = 0 ents no tenemos reset 

    if(counter <= limit_ref) begin      //cuento hasta el limite_ref = R2
       counter <= counter+1;            //incremeto el contador  
       valid <= 1'b0;                   //reseteo la salida de validacion del comparador para el shiftReg
    end    
    else begin 
        counter <={NB_COUNTER{1'b0}}; //reseta el contador
        valid = 1'b1;                 //Habilito la salida de validacion para el shiftReg
    end
    end
    else begin 
        counter <= counter; //No se genera cambio
        valid <= valid;     //no genero cambios hasta el prox pulso de relog
    end

end //fin de always()

//valor de salida
assign o_valid = valid;     //cable de salida para la señal habilitante que es entrada en el shiftReg

endmodule