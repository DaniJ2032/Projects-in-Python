/*PRIMER MODULO EN VERILOG*/
module top
#( 
    parameter   NB_SW = 4,
    parameter   NB_COUNTER = 32,
    parameter   NB_LEDS = 4
)

( 
    //output [3:0] o_led, o_led_b, o_led_g, --> No recomendable para codigos grandes
    output  [NB_LEDS-1:0] o_led,        
    output  [NB_LEDS-1:0] o_led_b,
    output  [NB_LEDS-1:0] o_led_g,

    input   [NB_SW-1:0] i_sw,
    input   i_reset,    clock
);

wire connect_count_to_shiftreg_valid; 
wire [NB_LEDS-1:0]conect_oleds_to_mux;
/*Instanciacion de los modulos count y shiftreg*/
count
#(
    .NB_SW  (NB_SW-1),
    .NB_COUNTER(NB_COUNTER)      
)
    u_count    
(
    //output [3:0] o_led, o_led_b, o_led_g, --> No recomendable para codigos grandes
    .o_valid(connect_count_to_shiftreg_valid),       
    .i_sw   (i_sw[NB_SW2-2:0]), //Conectamos solo 3 bit siguiendo el esquma de bloques
    .i_reset(i_reset), 
    .clock  (clock)
);

shiftreg
    #(.NB_LEDS(NB_LEDS)) 

    u_siftreg
(
    //output [3:0] o_led, o_led_b, o_led_g, --> No recomendable para codigos grandes
    .o_led  (conect_oleds_to_mux),       
    .i_valid(connect_count_to_shiftreg_valid),
    .i_reset(i_reset),
    .clock  (clock)

);

//Salidas
assign o_led = conect_oleds_to_mux;
assign o_led_g = (i_sw[3] == 1'b0) ? conect_oleds_to_mux: 4'b0000;
assign o_led_b = (i_sw[3] == 1'b1) ? conect_oleds_to_mux: 4'b0000;

endmodule