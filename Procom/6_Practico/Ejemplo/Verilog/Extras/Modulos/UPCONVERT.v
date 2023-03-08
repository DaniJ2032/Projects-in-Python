module upconverter (
    input i_out_PRBSQ,
    input i_out_PRBSI,

    output [3:0] o_out_UpConvertI,
    output [3:0] o_out_UpConvertQ
);

wire [3:0 ]out_Q;
wire [3:0 ]out_I;
//Por cada muestra de PRBS se generar 4 muestras en UpConvert donde una es
//es la salida de la PRBS y los demas son ceros    
assign out_Q = {i_out_PRBSQ,3'b000};
assign out_I = {i_out_PRBSI,3'b000};

assign o_out_UpConvertI = out_I;
assign o_out_UpConvertQ = out_Q;

endmodule