/*_____TP_4_Punto_A Instancia de modulos para leds_______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module count
#(  parameter NB_SW = 3, NB_COUNTER = 32 ) 
(
    output  o_valid,            //Salida de validacion de contador para los modulos
    input   [NB_SW - 1:0] i_sw, //Selector de los registros y enable del contador
    input   i_reset,            //Reset global
    input   clock               //Señal de clock
);

//Parametros locales
localparam R0 = 2**(NB_COUNTER-11);
localparam R1 = 2**(NB_COUNTER-12);   //Limite de tiempo el cual los led estaran prendidos 
localparam R2 = 2**(NB_COUNTER-13);
localparam R3 = 2**(NB_COUNTER-14);

//conexiones y registros
wire    [NB_COUNTER-1 : 0]  limit_ref;  
reg     [NB_COUNTER-1 : 0]  counter;    //Registro de contador
reg     valid;                          //registro de validacion del contador

//Descripcion del comparador
assign limit_ref = {i_sw[2:1] == 2'b00} ? R0 :  //Asigno el limite de referencia en el comparador
                   {i_sw[2:1] == 2'b01} ? R1 :
                   {i_sw[2:1] == 2'b10} ? R2 : R3;     
///////////////////

//Descripcion del contador
always @(posedge clock) begin 
    
    if(i_reset) begin
        counter <={NB_COUNTER{1'b0}};  
        valid <= 1'b0;                //reset de los registros
    end
    
    else if (i_sw[0]) begin  

    if(counter <= limit_ref) begin      
       counter <= counter+1;            //incremeto el contador  
       valid <= 1'b0;                   //reseteo la salida de validacion 
    end    
    else begin 
        counter <={NB_COUNTER{1'b0}}; //reseta el contador
        valid <= 1'b1;                 //Habilito la salida de validacion 
    end
    
    end
    else begin 
        counter <= counter; 
        valid <= valid;     //no genero cambios hasta el prox pulso de relog
    end

end //fin de always()

//Salida
assign o_valid = valid; //cable de salida para la señal habilitante 

endmodule



