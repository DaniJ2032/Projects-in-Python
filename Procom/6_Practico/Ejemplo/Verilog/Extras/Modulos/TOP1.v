//Prueba de Primer TOP

module TX_top (
    input   clock,    
    input   i_reset

);

wire input_to_up_convertI;
wire input_to_up_convertQ;
wire [3:0] output_to_up_convertI;
wire [3:0] output_to_up_convertQ;
wire valid_to_PRBS

//Instancia de los modulos

counter
    u_counter
(
    .clock          (clock),
    .i_enable       (1'b1),
    .i_reset        (i_reset),
    // .[2:0] o_counter(),
    .o_valid(valid_to_PRBS)
);


//PRBS Q e I
prbsQI 
    u_prbsQI
(
    .clock      (valid_to_PRBS),
    .i_reset    (~i_reset),
    .i_enable   (1'b1),
    .o_PRBSI    (input_to_up_convertI),
    .o_PRBSQ    (input_to_up_convertQ)
);

//upconverter       ##REVISAR¡¡¡¡¡
upconverter 
    u_upconverter
(
    .i_out_PRBSQ        (input_to_up_convertQ ),
    .i_out_PRBSI        (input_to_up_convertI ),
    .o_out_UpConvertI   (output_to_up_convertI),
    .o_out_UpConvertQ   (output_to_up_convertQ)
);


endmodule