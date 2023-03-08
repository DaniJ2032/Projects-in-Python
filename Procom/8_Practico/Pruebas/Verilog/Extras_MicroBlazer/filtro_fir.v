//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo Filtro Q e I proporciona las dos salidas de ambos  
//
//////////////////////////////////////////////////////////////////////////////////

module filtro_firQI
  #(
    parameter NB_OUTPUT  = 8, //! NB of output
    parameter NBF_OUTPUT = 6, //! NBF of output
    parameter NB_COEFF   = 8, //! NB of Coefficients
    parameter NBF_COEFF  = 6  //! NBF of Coefficients
     
  ) 
  (
    input                         clock,    //! Clock
    input                         i_reset,  //! Reset
    input                         i_enable, //! Enable
    input                         i_valid,
    input                         i_dataPrbsI, //! Input Sample
    input                         i_dataPrbsQ, 
    input [2:0]                   i_counterMux,

    output signed [NB_OUTPUT-1:0] o_out_firI, //! Output Sample
    output signed [NB_OUTPUT-1:0] o_out_firQ  
  );
  /*Parámetros Locales*/
  localparam NB_ADD     = NB_COEFF  + 3; //3 bits para las 6 sumas
  localparam NBF_ADD    = NBF_COEFF;
  localparam NBI_ADD    = NB_ADD    - NBF_ADD;
  localparam NBI_OUTPUT = NB_OUTPUT - NBF_OUTPUT;
  localparam NB_SAT     = (NB_ADD-NBF_ADD)-(NB_OUTPUT-NBF_OUTPUT);

  /*Matriz de coeficientes del filtro Q e I*/
  wire  signed [NB_COEFF-1:0] Coeficientes [23:0]; //! Matrir for Coefficients

  /*Registros y cables para el FIR I*/ 
  wire  signed [NB_COEFF-1:0] signedCoefI  [5: 0];
  wire  signed [NB_COEFF-1:0] out_muxI     [5: 0];
  wire  signed [NB_ADD - 1:0] sumI;
  reg  [5:0]                  registerI;

  /*Registros y cables para el FIR Q*/
  wire  signed [NB_COEFF-1:0] signedCoefQ  [5: 0];
  wire  signed [NB_COEFF-1:0] out_muxQ     [5: 0];
  wire  signed [NB_ADD - 1:0] sumQ;
  reg  [5:0]                  registerQ;
    
  // Coeficientes
  assign Coeficientes[23] = 8'b0000_0000;//8'b0000_0000;//8'b0000_0000;
  assign Coeficientes[22] = 8'b0000_0001;//8'b0000_0000;//8'b0000_0000;
  assign Coeficientes[21] = 8'b0000_0001;//8'b0000_0000;//8'b0000_0001;
  assign Coeficientes[20] = 8'b0000_0000;//8'b0000_0001;//8'b0000_0001;
  assign Coeficientes[19] = 8'b1111_1100;//8'b0000_0000;//8'b0000_0000;
  assign Coeficientes[18] = 8'b1111_1000;//8'b0000_0000;//8'b1111_1100;
  assign Coeficientes[17] = 8'b1111_1000;//8'b0000_0000;//8'b1111_1000;
  assign Coeficientes[16] = 8'b0000_0000;//8'b0000_0001;//8'b1111_1000;
  assign Coeficientes[15] = 8'b0001_0001;//8'b0000_0000;//8'b0000_0000;
  assign Coeficientes[14] = 8'b0010_0110;//8'b0000_0000;//8'b0001_0001;
  assign Coeficientes[13] = 8'b0011_1001;//8'b0000_0000;//8'b0010_0110;
  assign Coeficientes[12] = 8'b0100_0000;//8'b0000_0001;//8'b0011_1001;
  assign Coeficientes[11] = 8'b0011_1001;//8'b0000_0000;//8'b0100_0000;
  assign Coeficientes[10] = 8'b0010_0110;//8'b0000_0000;//8'b0011_1001;
  assign Coeficientes[9]  = 8'b0001_0001;//8'b0000_0000;//8'b0010_0110;
  assign Coeficientes[8]  = 8'b0000_0000;//8'b0000_0001;//8'b0001_0001;
  assign Coeficientes[7]  = 8'b1111_1000;//8'b0000_0000;//8'b0000_0000;
  assign Coeficientes[6]  = 8'b1111_1000;//8'b0000_0000;//8'b1111_1000;
  assign Coeficientes[5]  = 8'b1111_1100;//8'b0000_0000;//8'b1111_1000;
  assign Coeficientes[4]  = 8'b0000_0000;//8'b0000_0001;//8'b1111_1100;
  assign Coeficientes[3]  = 8'b0000_0001;//8'b0000_0000;//8'b0000_0000;
  assign Coeficientes[2]  = 8'b0000_0001;//8'b0000_0000;//8'b0000_0001;
  assign Coeficientes[1]  = 8'b0000_0000;//8'b0000_0000;//8'b0000_0001;
  assign Coeficientes[0]  = 8'b0000_0000;//8'b0000_0001;//8'b0000_0000;
  
  integer ptr1;
  //! ShiftRegister model a clock de PRBS el mas lento 
  always @(posedge clock) begin:shiftRegister
    if (i_reset) begin
      registerI <= 0;
      registerQ <= 0;
    end else if (i_enable && i_counterMux == 2'b01) begin

      registerI[5] <= i_dataPrbsI;
      registerI[4] <= registerI[5];
      registerI[3] <= registerI[4];
      registerI[2] <= registerI[3];
      registerI[1] <= registerI[2];
      registerI[0] <= registerI[1];

      registerQ[5] <= i_dataPrbsQ;
      registerQ[4] <= registerQ[5];
      registerQ[3] <= registerQ[4];
      registerQ[2] <= registerQ[3];
      registerQ[1] <= registerQ[2];
      registerQ[0] <= registerQ[1];
    end        
  end  
      /*______Mux para FIR I______*/
      /*Asignamos la salida de los datos de los muxI dependiendo el valor del contador del mismo*/  
      assign out_muxI[5] = (i_counterMux == 2'b10) ? Coeficientes[0]  : (i_counterMux == 2'b11) ? Coeficientes[1]  : (i_counterMux == 2'b00) ? Coeficientes[2]  :  Coeficientes[3] ;
      assign out_muxI[4] = (i_counterMux == 2'b10) ? Coeficientes[4]  : (i_counterMux == 2'b11) ? Coeficientes[5]  : (i_counterMux == 2'b00) ? Coeficientes[6]  :  Coeficientes[7] ;
      assign out_muxI[3] = (i_counterMux == 2'b10) ? Coeficientes[8]  : (i_counterMux == 2'b11) ? Coeficientes[9]  : (i_counterMux == 2'b00) ? Coeficientes[10] :  Coeficientes[11];
      assign out_muxI[2] = (i_counterMux == 2'b10) ? Coeficientes[12] : (i_counterMux == 2'b11) ? Coeficientes[13] : (i_counterMux == 2'b00) ? Coeficientes[14] :  Coeficientes[15];
      assign out_muxI[1] = (i_counterMux == 2'b10) ? Coeficientes[16] : (i_counterMux == 2'b11) ? Coeficientes[17] : (i_counterMux == 2'b0)  ? Coeficientes[18] :  Coeficientes[19];
      assign out_muxI[0] = (i_counterMux == 2'b10) ? Coeficientes[20] : (i_counterMux == 2'b11) ? Coeficientes[21] : (i_counterMux == 2'b00) ? Coeficientes[22] :  Coeficientes[23];
      
      /*Dependiendo del dato de PRBSI tomaremos signo negativo o positivo*/
      assign signedCoefI [0] = (registerI[0] == 0) ? out_muxI[0]  : (-out_muxI[0]);
      assign signedCoefI [1] = (registerI[1] == 0) ? out_muxI[1]  : (-out_muxI[1]);
      assign signedCoefI [2] = (registerI[2] == 0) ? out_muxI[2]  : (-out_muxI[2]);
      assign signedCoefI [3] = (registerI[3] == 0) ? out_muxI[3]  : (-out_muxI[3]);
      assign signedCoefI [4] = (registerI[4] == 0) ? out_muxI[4]  : (-out_muxI[4]);
      assign signedCoefI [5] = (registerI[5] == 0) ? out_muxI[5]  : (-out_muxI[5]);

      /*______Mux para FIR Q______*/
      /*Asignamos la salida de los datos de los muxI dependiendo el valor del contador del mismo*/  
      assign out_muxQ[5] = (i_counterMux == 2'b10) ? Coeficientes[0]  : (i_counterMux == 2'b11) ? Coeficientes[1]  : (i_counterMux == 2'b00) ? Coeficientes[2]  :  Coeficientes[3] ;
      assign out_muxQ[4] = (i_counterMux == 2'b10) ? Coeficientes[4]  : (i_counterMux == 2'b11) ? Coeficientes[5]  : (i_counterMux == 2'b00) ? Coeficientes[6]  :  Coeficientes[7] ;
      assign out_muxQ[3] = (i_counterMux == 2'b10) ? Coeficientes[8]  : (i_counterMux == 2'b11) ? Coeficientes[9]  : (i_counterMux == 2'b00) ? Coeficientes[10] :  Coeficientes[11];
      assign out_muxQ[2] = (i_counterMux == 2'b10) ? Coeficientes[12] : (i_counterMux == 2'b11) ? Coeficientes[13] : (i_counterMux == 2'b00) ? Coeficientes[14] :  Coeficientes[15];
      assign out_muxQ[1] = (i_counterMux == 2'b10) ? Coeficientes[16] : (i_counterMux == 2'b11) ? Coeficientes[17] : (i_counterMux == 2'b0)  ? Coeficientes[18] :  Coeficientes[19];
      assign out_muxQ[0] = (i_counterMux == 2'b10) ? Coeficientes[20] : (i_counterMux == 2'b11) ? Coeficientes[21] : (i_counterMux == 2'b00) ? Coeficientes[22] :  Coeficientes[23];
      
      /*Dependiendo del dato de PRBSI tomaremos signo negativo o positivo*/
      assign signedCoefQ [0] = (registerQ[0] == 0) ? out_muxQ[0]  : (-out_muxQ[0]);
      assign signedCoefQ [1] = (registerQ[1] == 0) ? out_muxQ[1]  : (-out_muxQ[1]);
      assign signedCoefQ [2] = (registerQ[2] == 0) ? out_muxQ[2]  : (-out_muxQ[2]);
      assign signedCoefQ [3] = (registerQ[3] == 0) ? out_muxQ[3]  : (-out_muxQ[3]);
      assign signedCoefQ [4] = (registerQ[4] == 0) ? out_muxQ[4]  : (-out_muxQ[4]);
      assign signedCoefQ [5] = (registerQ[5] == 0) ? out_muxQ[5]  : (-out_muxQ[5]);


      /*Sumatoria de los cpoeficientes Q e I*/
      assign sumI = signedCoefI[0] + signedCoefI[1] + signedCoefI[2] + signedCoefI[3] + signedCoefI[4] + signedCoefI[5];
      assign sumQ = signedCoefQ[0] + signedCoefQ[1] + signedCoefQ[2] + signedCoefQ[3] + signedCoefQ[4] + signedCoefQ[5];

      /*Salida FIR I*/
      assign o_out_firI = ( ~|sumI[NB_ADD-1 -: NB_SAT+1] || &sumI[NB_ADD-1 -: NB_SAT+1]) ? sumI[NB_ADD-(NBI_ADD-NBI_OUTPUT) - 1 -: NB_OUTPUT] :
                    (sumI[NB_ADD-1]) ? {{1'b1},{NB_OUTPUT-1{1'b0}}} : {{1'b0},{NB_OUTPUT-1{1'b1}}};

      /*Salida FIR Q*/
      assign o_out_firQ = ( ~|sumQ[NB_ADD-1 -: NB_SAT+1] || &sumQ[NB_ADD-1 -: NB_SAT+1]) ? sumQ[NB_ADD-(NBI_ADD-NBI_OUTPUT) - 1 -: NB_OUTPUT] :
                    (sumQ[NB_ADD-1]) ? {{1'b1},{NB_OUTPUT-1{1'b0}}} : {{1'b0},{NB_OUTPUT-1{1'b1}}};    
        
endmodule

