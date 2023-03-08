/*_____TP_4_Punto_A Instancia de modulos para leds_______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module top
#(  parameter  NB_SW = 4, NB_BTN = 4, NB_COUNTER = 32, NB_LEDS = 4  ) //parametros
( 
    // Comentar hasta i_reset si se usa modulo vio
   output  [NB_LEDS-1:0] o_led,    //Led comunes        
   output  [NB_LEDS-1:0] o_led_b,     
   output  [NB_LEDS-1:0] o_led_g,  //led RGB
   output  [NB_LEDS-1:0] o_led_r,

   input   [NB_SW-1:0]   i_sw,     //4bit pra el selector
   input   [NB_BTN-1:0]  i_btn,    //4bit para la botonera 
   input   i_reset,
    /////////////////////////   
    input   clock                  //clock
);

//Cables para el uso del vio
//     wire  [NB_LEDS - 1 : 0] o_led;
//     wire  [NB_LEDS - 1 : 0] o_led_b;
//     wire  [NB_LEDS - 1 : 0] o_led_g;
//     wire  [NB_LEDS - 1 : 0] o_led_r;
//     wire  [NB_SW   - 1 : 0] i_sw;
//     wire  [NB_BTN  - 1 : 0] i_btn;
//     wire  i_reset;
/////////////////////////

//Conexiones entre los modulos y salidas del top
wire    connect_count_to_valid;                  //validacion para los modulos
wire    connect_count_to_shifreg_valid; 
wire    [NB_LEDS-1:0]   conect_oleds_SR_to_mux;  //conexion de los diferentes modos
wire    [NB_LEDS-1:0]   conect_oleds_FS_to_mux;

//Registros
reg     [NB_LEDS-1:0]   reg_oled_to_mux;
reg                     reg_btn;       //modo shifter o Flash
reg                     reg_modo;        
reg     [NB_LEDS-1:0]   reg_color_mode;  
/////////////////////////////////////

/*Instanciacion de los modulos count, shiftreg y flashreg*/

//Modulo count
count   
#( .NB_SW  (NB_SW-1), .NB_COUNTER(NB_COUNTER) )       
   
    u_count    
(
    .o_valid    (connect_count_to_valid),         
    .i_sw       (i_sw[NB_SW-2:0]),         
    .i_reset    (~i_reset), 
    .clock      (clock)
);

//Modulo shiftreg
shiftreg
    #(.NB_LEDS(NB_LEDS)) 

    u_siftreg
(
    .o_SR_led   (conect_oleds_SR_to_mux),
    .o_valid    (connect_count_to_shifreg_valid),

    .i_sw       (i_sw[NB_SW-1]),    //solo pasamos el i_sw[3]       
    .i_valid    (connect_count_to_valid),
    .i_reset    (~i_reset),
    .clock      (clock)
);

//Modulo flashreg
flashReg
    #(.NB_LEDS (NB_LEDS))

    u_flashreg  
(
    .o_FS_led   (conect_oleds_FS_to_mux),                    
    .i_valid    (connect_count_to_shifreg_valid),    
    .i_reset    (~i_reset),                          
    .clock      (clock)                              
);

//Salidas del modulo top (Conexion del mux) siguiendo el esquema de bloques

//Detector de flancos para cambiar entre los dos modos
always @(posedge clock) begin
    
    if(~i_reset) begin
        reg_btn         <= 1'b0;       
        reg_modo        <= 1'b0;
    end
    else begin
        reg_btn <= i_btn[0];

        if(!reg_btn && i_btn[0]) begin
            reg_modo <= ~reg_modo;      //Cambio entre los modos FS y SR        
        end

         if (reg_modo) begin
            reg_oled_to_mux <= conect_oleds_SR_to_mux;  //conexion salida SR
        end
         else begin
            reg_oled_to_mux <= conect_oleds_FS_to_mux;  //conexion salida FS
        end
    end 
end     //fin de always

//Cambio de colores de los led RGB
always @(posedge clock) begin

    if(~i_reset) begin
        reg_color_mode  <= 3'b001;  //Rojo por defecto
    end
    else begin

        if(i_btn[1]) begin
            reg_color_mode <= 3'b001;   //Color Rojo
        end
        else if(i_btn[2]) begin
            reg_color_mode <= 3'b010;   //Color Azul
        end
        else if(i_btn[3]) begin
            reg_color_mode <= 3'b100;   //Color Verde
        end                
    end 
end
    
assign  o_led    = {reg_color_mode,reg_modo};
assign  o_led_r  = (reg_color_mode[0]) ? reg_oled_to_mux : 4'b0000;
assign  o_led_b  = (reg_color_mode[1]) ? reg_oled_to_mux : 4'b0000;
assign  o_led_g  = (reg_color_mode[2]) ? reg_oled_to_mux : 4'b0000;

//Instanciacion del modulo virtual VIO
//      vio
//      u_vio
//          (
//          .clk_0       (clock),
//          .probe_in0_0 (o_led),
//          .probe_in1_0 (o_led_b),
//          .probe_in2_0 (o_led_g),
//          .probe_in3_0 (o_led_r),
        
//          .probe_out0_0(i_reset),
//          .probe_out1_0(i_btn),
//          .probe_out2_0(i_sw) 
//          );

endmodule