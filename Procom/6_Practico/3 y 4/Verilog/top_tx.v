module top_tx
#(
  parameter NB_OUTPUT  = 8, //! NB of output
  parameter NBF_OUTPUT = 6, //! NBF of output
  parameter NB_COEFF   = 8, //! NB of Coefficients
  parameter NBF_COEFF  = 6, //! NBF of Coefficients
  parameter NBAUDS     = 6 //! Baudios del filtro 

)
(
    input         clock,
    //Comentados para el uso del vio
    // input         i_reset,
    // input   [3:0] i_sw, //i_sw[0] para PRBS y FIR, i_sw[1] para BER, i_sw[3:2] selec de fase
    output  [3:0] o_led //o_led[0] para reset , o_led[1] para PRBS y FIR , o_led[2] para el BER , o_led[3] Indica el fin de fase de seteo
);

  //Salidas del contador 
  wire [2:0] counter_to_mux;
  wire valid_to_Prbs;

  //Salidas de PRBS
  wire out_prbsI_to_fir;  
  wire out_prbsQ_to_fir;

  //Salida de los Filtros Q e I
  wire signed [NB_OUTPUT-1:0] out_data_firI;
  wire signed [NB_OUTPUT-1:0] out_data_firQ; 

  //Salida de los SLicer Q e I
  wire output_to_signedI;
  wire output_to_signedQ;

  //Salida de los contadores de BER Q e I
  wire output_faseOkI;
  wire output_faseOkQ;

  //Conexiones para el VIO
  wire        i_reset ;
  wire  [3:0] i_sw    ; 

  //Salidas para monitorear los contadores de BER de Q e I
  //Q
  wire          out_to_exorQ      ;
  wire [63:0]   out_to_counterBitQ;
  wire [63:0]   out_to_counterErrQ;
  //I
  wire          out_to_exorI      ;
  wire [63:0]   out_to_counterBitI;
  wire [63:0]   out_to_counterErrI;

  //Registro para manejo de los led indicadores
  reg [3:0] regLedOut;

  counter
    u_counter
      (
        .clock    (clock),
        .i_reset  (~i_reset),
        .i_enable (i_sw[0]),

        .o_counter_mux (counter_to_mux),  //Contador para el mux del FIR
        .o_validPrbs (valid_to_Prbs)      //Clock para PRBS y FIR
      );

  prbsQI
  u_prbsQI
    (
      .clock    (clock),
      .i_reset  (~i_reset),
      .i_enable (i_sw[0]),
      .i_valid  (valid_to_Prbs),
      .o_PrbsI  (out_prbsI_to_fir),
      .o_PrbsQ  (out_prbsQ_to_fir)

    );

   filtro_firQI
     #(
       .NB_OUTPUT  (NB_OUTPUT), //! NB of output
       .NBF_OUTPUT (NBF_OUTPUT), //! NBF of output
       .NB_COEFF   (NB_COEFF), //! NB of Coefficients
       .NBF_COEFF  (NBF_COEFF),  //! NBF of Coefficients
       .NBAUDS     (NBAUDS)
     )
     u_filtro_firQI 
       (
         .clock        (clock),          //! Clock
         .i_reset      (~i_reset),      //! Reset
         .i_enable     (i_sw[0]),       //! Enable
         .i_valid      (valid_to_Prbs),       
         .i_dataPrbsI  (out_prbsI_to_fir), //! Input Sample
         .i_dataPrbsQ  (out_prbsQ_to_fir), 
         .i_counterMux (counter_to_mux),

         .o_out_firI   (out_data_firI),
         .o_out_firQ   (out_data_firQ)      //! Output Sample
       );
      
  FaseAndSlicerQI
    u_FaseAndSlicerQI
      (
        .clock          (clock            ),
        .i_reset        (~i_reset         ),
        .i_enable       (i_sw[0]          ),
        .i_firI         (out_data_firI    ),
        .i_firQ         (out_data_firQ    ),        
        .i_valid        (valid_to_Prbs    ),
        .i_selector     (i_sw[3:2]        ), 

        .output_slicerI (output_to_signedI),
        .output_slicerQ (output_to_signedQ)       
      );
      
  CounterBerI
    u_CounterBerI
      (
        .clock        (clock),
        .i_reset      (~i_reset),
        .i_enable     (i_sw[1]),
        .i_firI       (output_to_signedI),
        .i_prbsI      (out_prbsI_to_fir),
        .i_valid      (valid_to_Prbs), 

        .o_exorI       (out_to_exorI      ),     
        .o_counterBitI (out_to_counterBitI),
        .o_counterErrI (out_to_counterErrI),
        .o_FaseSetOkI  (output_faseOkI    )    
      );

  CounterBerQ
    u_CounterBerQ
      (
        .clock         (clock),
        .i_reset       (~i_reset),
        .i_enable      (i_sw[1]),
        .i_firQ        (output_to_signedQ),
        .i_prbsQ       (out_prbsQ_to_fir),
        .i_valid       (valid_to_Prbs),

        .o_exorQ       (out_to_exorQ      ),     
        .o_counterBitQ (out_to_counterBitQ),
        .o_counterErrQ (out_to_counterErrQ),
        .o_FaseSetOkQ  (output_faseOkQ)      
      );

//Instancia de VIO e ILA

VIO
  u_VIO
  (
    .clk_0        (clock),
    .probe_in0_0  (o_led),
    .probe_in1_0  (out_to_exorQ),
    .probe_in2_0  (out_to_exorI),
    .probe_in3_0  (out_to_counterBitQ),
    .probe_in4_0  (out_to_counterBitI),
    .probe_in5_0  (out_to_counterErrQ),
    .probe_in6_0  (out_to_counterErrI),    
    .probe_out0_0 (i_reset),
    .probe_out1_0 (i_sw)
  );

ILA
  u_ILA
  (
    .clk_0    (clock),
    .probe0_0 (o_led),
    .probe1_0 (out_data_firI),
    .probe2_0 (out_data_firQ)
  );

  /*____Salida de los led____*/
  always @(posedge clock) begin

    if(~i_reset)begin
    regLedOut <= 4'b0001; //Led 0 indica reset activado

    end else begin
                  regLedOut      [0] <= 1'b0;   
      if(i_sw[0]) regLedOut      [1] <= 1'b1;
      else        regLedOut      [1] <= 1'b0;        

      if(i_sw[1]) regLedOut      [2] <= 1'b1;
      else        regLedOut      [2] <= 1'b0;

      if(output_faseOkI) regLedOut[3] <= 1'b1;
      else        regLedOut      [3] <= 1'b0;

    end
  end

  assign o_led[0] = regLedOut [0];
  assign o_led[1] = regLedOut [1];  //Asigno la salida de los led
  assign o_led[2] = regLedOut [2];
  assign o_led[3] = regLedOut [3];

endmodule
