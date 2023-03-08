/*_____TP_4_Punto_B Agregamos un 3er barrido de leds______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module shiftreg2led 
#(  parameter NB_LEDS = 4 ) 
(
    output  [NB_LEDS-1:0] o_SR2L_led,

    input   i_sw,
    input   i_btn,
    input   i_valid,
    input   i_reset,    
    input   clock
);
    
//registros
reg [NB_LEDS-1:0] shiftreg2led;
reg reg_btn; 
reg [1:0]count;  

//Descripcion del Shiftreg2led
always @(posedge clock) begin

if(i_reset) begin               
        reg_btn      <= 1'b0; 
        count        <= 2'b00;   //Reseteo de variables           
        shiftreg2led <= 4'b1001;  
  
    end 
    else begin

        //conteo del boton
        reg_btn <= i_btn;    
        if(reg_btn == 1'b0 && i_btn == 1'b1)
            count <= count + 2'b01; //incremento el contador
        else if(count == 2'b11)
            count <= 2'b00;      //reseteo el contador
        else 
            count <= count;

        if(i_valid == 1'b1 && i_sw == 1'b0 && count == 2'b10) begin
            if(shiftreg2led == 4'b0000)
                shiftreg2led <= 4'b1001;    //Despalzo desde los extremos
            else 
                shiftreg2led <= {1'b0,shiftreg2led[3],shiftreg2led[0],1'b0}; 
        end

        else if(i_valid == 1'b1 && i_sw == 1'b1 && count == 2'b10)begin   
            if (shiftreg2led == 4'b0000)
                shiftreg2led <= 4'b0110;    //Despalzo desde el centro
            else
                shiftreg2led <= {shiftreg2led[NB_LEDS-2],1'b0,1'b0,shiftreg2led[NB_LEDS-3]};
        end

        else begin    
            shiftreg2led <= shiftreg2led;
        end
        
    end //fin de else   
end //fin del always    

//Salida
assign  o_SR2L_led = shiftreg2led;

endmodule