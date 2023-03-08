/*_____TP_4_Punto_B Agregamos un 3er barrido de leds______
*Autor: Daniel Juarez                                    *                  
*Fecha: 04/06/2021                                       *
*________________________________________________________*
*/
module top
#(  parameter  NB_SW = 4, NB_BTN = 4, NB_COUNTER = 32, NB_LEDS = 4  )
( 
    //Para el uso del vio comentar hasta el i_reset
   output  [NB_LEDS-1:0] o_led,    //Led comunes        
   output  [NB_LEDS-1:0] o_led_b,     
   output  [NB_LEDS-1:0] o_led_g,  //led RGB
   output  [NB_LEDS-1:0] o_led_r,

   input   [NB_SW-1:0]   i_sw,     //4bit pra el selector
   input   [NB_BTN-1:0]  i_btn,    //4bit para la botonera 
   input   i_reset,
    //////////////////////////////   
    input   clock                   // clock
);

//Wire para el uso del vio
//     wire  [NB_LEDS - 1 : 0] o_led;
//     wire  [NB_LEDS - 1 : 0] o_led_b;
//     wire  [NB_LEDS - 1 : 0] o_led_g;
//     wire  [NB_LEDS - 1 : 0] o_led_r;
//     wire  [NB_SW   - 1 : 0] i_sw;
//     wire  [NB_BTN  - 1 : 0] i_btn;
//     wire  i_reset;
/////////////////////////


//Conexiones internas entre bloques
wire    connect_count_to_valid;         //Cables de validacion
wire    connect_count_to_shifreg_valid; 
wire    connect_count_to_flashreg_valid;

//Cables para la salida del top a traves del mux de los led 
wire    [NB_LEDS-1:0]   conect_oleds_SR_to_mux;  //para conectar los led en los diferentes modos
wire    [NB_LEDS-1:0]   conect_oleds_FS_to_mux;
wire    [NB_LEDS-1:0]   conect_oleds_SR2L_to_mux;

//Registros 
reg                     reg_btn;           //para detectar el boton
reg     [1:0]           reg_modo;          //modo Shift, Shift2led o flash
reg     [NB_LEDS-1:0]   reg_oled_to_mux;   //Registro de salida para el color 
reg     [NB_LEDS-1:0]   reg_color_mode;    //Registro de salida para el mux
/////////////////////////////////////

/*Instanciacion de los modulos count, shiftreg, shiftreg2led y flashreg*/

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

    .i_sw       (i_sw[NB_SW-1]),    //solo pasamos el i_sw [3]   
    .i_btn      (i_btn[0]     ),    //solo pasamos el i_btn[0]
    .i_valid    (connect_count_to_valid),
    .i_reset    (~i_reset),
    .clock      (clock)
);

//Modulo shiftreg2led
shiftreg2led
    #(.NB_LEDS(NB_LEDS)) 

    u_shiftreg2led
(
    .o_SR2L_led   (conect_oleds_SR2L_to_mux),

    .i_sw       (i_sw[NB_SW-1]),      
    .i_btn      (i_btn[0]     ),    
    .i_valid    (connect_count_to_flashreg_valid),
    .i_reset    (~i_reset),
    .clock      (clock)
);

//Modulo flashreg
flashReg
    #(.NB_LEDS (NB_LEDS))

    u_flashreg  
(
    .o_FS_led   (conect_oleds_FS_to_mux),           
    .o_valid    (connect_count_to_flashreg_valid),        
    .i_valid    (connect_count_to_shifreg_valid),    
    .i_reset    (~i_reset),                          
    .clock      (clock)                              
);

//Salidas del modulo top (Conexion del mux) siguiendo el esquema de bloques

//Detector de flancos para cambiar entre los 3 modos
always @(posedge clock) begin
    
    if(~i_reset) begin
        reg_btn     <= 1'b0;       
        reg_modo    <= 1'b0;
    end
    else begin
        reg_btn <= i_btn[0];

        if(!reg_btn && i_btn[0]) begin
            reg_modo <= reg_modo + 2'b01;   
        end
         else if (reg_modo == 2'b11) begin
            reg_modo <= 2'b00;
        end
        else begin
            reg_modo <= reg_modo; 
        end
        //////Eleccion de los modos
         if (reg_modo == 2'b00) begin                    
            reg_oled_to_mux <= conect_oleds_FS_to_mux;   //Modo FS
        end
        else if (reg_modo == 2'b01)begin                        
            reg_oled_to_mux <= conect_oleds_SR_to_mux;   //Modo SR
        end
        else begin
            reg_oled_to_mux <= conect_oleds_SR2L_to_mux; //Modo SR2L
        end
    end 
end     //fin de always

//Seleccion del color de los led de salida
always @(posedge clock) begin

    if(~i_reset) begin
        reg_color_mode  <= 3'b001;  //Color rojo por defecto
    end
    else begin
        if(i_btn[1]) begin
            reg_color_mode <= 3'b001;   //Color rojo       
        end
        else if(i_btn[2]) begin
            reg_color_mode <= 3'b010;   //Color azul
        end
        else if(i_btn[3]) begin
            reg_color_mode <= 3'b100;   //Color verde
        end                
    end 
end     //fin de always
 
//Salidas del top     
assign  o_led    = {reg_color_mode,reg_modo};
assign  o_led_r  = (reg_color_mode[0]) ? reg_oled_to_mux : 4'b0000;
assign  o_led_b  = (reg_color_mode[1]) ? reg_oled_to_mux : 4'b0000;
assign  o_led_g  = (reg_color_mode[2]) ? reg_oled_to_mux : 4'b0000;

    //Instanciacion del modulo virtual VIO
//    vio
//    u_vio
//      (
//      .clk_0       (clock),
//      .probe_in0_0 (o_led),
//      .probe_in1_0 (o_led_b),
//      .probe_in2_0 (o_led_g),
//      .probe_in3_0 (o_led_r),
    
//      .probe_out0_0(i_reset),
//      .probe_out1_0(i_btn),
//      .probe_out2_0(i_sw) 
//      );

endmodule