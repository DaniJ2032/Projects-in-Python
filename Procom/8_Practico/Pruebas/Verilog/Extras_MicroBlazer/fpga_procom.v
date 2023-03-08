//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Modulo FPGA Procom, es el TOP global abarcando todos los demas bloques  
//
//////////////////////////////////////////////////////////////////////////////////

module top
( 
//Descomentar para testeo
//    input   clockdsp,
//    input   [31 : 0] gpo0,
//    output  [31 : 0] gpi0,
//    input   i_reset,
//    input   testeo_datos,
//    output  [7 : 0] o_filtroQ,
//    output  [7 : 0] o_filtroI
///////////////////////////////
    input  clock100   ,
    input  in_reset   ,
    input  in_rx_uart ,
    output out_tx_uart      
);
  
  parameter NB_OUTPUT       = 8            ; //! NB of output
  parameter NBF_OUTPUT      = 6            ; //! NBF of output
  parameter NB_COEFF        = 8            ; //! NB of Coefficients
  parameter NBF_COEFF       = 6            ; //! NBF of Coefficients
  parameter NB_GPIOS        = 32           ;
  parameter RAM_WIDTH       = 32           ;            
  parameter RAM_DEPTH       = 32000        ;                  
  parameter RAM_PERFORMANCE = "LOW_LATENCY";
  parameter INIT_FILE       = ""           ;
  
  
  ///////////////////////////////////////////
  // Vars //comentar para prueba 
  ///////////////////////////////////////////
  wire [NB_GPIOS- 1 : 0] gpo0       ;
  wire [NB_GPIOS- 1 : 0] gpi0       ;
  wire                   locked     ;
  wire                   soft_reset ;
  wire                   clockdsp   ; 
  wire                   i_reset    ; 
  
  ///////////////////////////////////////////
  wire        [3          :0] i_sw           ; //i_sw[0] para PRBS y FIR, i_sw[1] para BER, i_sw[3:2] selec de fase
  wire        [3          :0] o_led          ; 
  wire signed [NB_OUTPUT-1:0] o_FIRQ         ; 
  wire signed [NB_OUTPUT-1:0] o_FIRI         ; 
  wire        [63         :0] o_ErrorQ       ;
  wire        [63         :0] o_ErrorI       ;
  wire        [63         :0] o_BitQ         ;
  wire        [63         :0] o_BitI         ;
  wire        [31         :0] o_mux_ErrorBits;
  wire                        salida_captura ;
  wire                        salida_read    ;
  wire                        i_EnILA        ;
  wire                        testeo_datos   ;
  wire        [7          :0] o_filtroQ      ;
  wire        [7          :0] o_filtroI      ;
  ///////////////////////////////////////////
  
  wire [RAM_WIDTH - 1 :0] Dato_input  ;
  wire [RAM_WIDTH - 1 :0] Dato_output ;
  
  ///////////////////////////////////////////
  // Registros RegisterFILE
  ///////////////////////////////////////////
  reg          o_reset       ;
  reg  [3 : 0] reg_i_sw      ;
  reg  [63: 0] ErrorQ        ;
  reg  [63: 0] ErrorI        ;
  reg  [63: 0] BitQ          ;
  reg  [63: 0] BitI          ;
  reg          logeo         ;
  reg          read          ;
  reg  [2 : 0] flag_E_B      ;
  reg          flag_captura  ;
  reg          captura       ;
  reg [31 : 0] direccion     ;

  ///////////////////////////////////////////
  // Bloque DSP
  ///////////////////////////////////////////
  top_tx
   #(
       .NB_OUTPUT  (NB_OUTPUT ),//! NB of output
       .NBF_OUTPUT (NBF_OUTPUT),//! NBF of output
       .NB_COEFF   (NB_COEFF  ),//! NB of Coefficients
       .NBF_COEFF  (NBF_COEFF ) //! NBF of Coefficients
       
     )
      u_top_tx
        (
          .clock     (clockdsp),
          .i_reset   (o_reset ),
          .i_sw      (reg_i_sw),
          .o_led     (o_led   ),
          .o_firI    (o_FIRI  ),
          .o_firQ    (o_FIRQ  ),
          .o_Error_I (o_ErrorI),
          .o_Error_Q (o_ErrorQ),
          .o_bits_I  (o_BitI  ),
          .o_bits_Q  (o_BitQ  ) 
        );   

  ///////////////////////////////////////////
  // MicroBlaze
  ///////////////////////////////////////////
  MicroGPIO
     u_MicroGPIO
     (
        .clock100         (clockdsp    ),  // Clock aplicacion
        .gpio_rtl_tri_o   (gpo0        ),  // GPIO
        .gpio_rtl_tri_i   (gpi0        ),  // GPIO
        .o_lock_clock     (locked      ),  // Senal Lock Clock        
        .reset            (in_reset    ),  // Hard Reset
        .sys_clock        (clock100    ),  // Clock de FPGA
        .usb_uart_rxd     (in_rx_uart  ),  // UART
        .usb_uart_txd     (out_tx_uart )   // UART
      );

  ///////////////////////////////////////////
  // FSM RAM
  ///////////////////////////////////////////  
  logeo
    u_logeo
     (
      .clock      (clock100),
      .En_logeo   (logeo),
      .i_adress   (direccion),
      .En_read    (read),
      .datos_input(Dato_input),
      .i_reset    (i_reset),
      .o_dato     (Dato_output)
      );

  ///////////////////////////////////////////
  // VIO e ILA
  ///////////////////////////////////////////    
  VIO
    u_VIO
    (
     .clk_0         (clock100 ),
     .probe_out0_0  (i_reset  )
     );
  ////////////////////////////////////////////   
  ila
   u_ila
    (
     .clk_0    (clock100),
     .probe0_0 (o_FIRI),
     .probe1_0 (o_FIRQ),
     .probe2_0 (Dato_output),
     .probe3_0 (o_filtroQ),
     .probe4_0 (o_filtroI)
     );

  ///////////////////////////////////////////
  // RegisterFILE
  ///////////////////////////////////////////

  always @(posedge clock100) begin //clock100
     if(i_reset == 1'b1) begin
        o_reset      <= 1'b1   ;
        reg_i_sw     <= 4'b0000;
        logeo        <= 1'b0   ;
        read         <= 1'b0   ;
        ErrorQ       <= 64'b0  ;
        ErrorI       <= 64'b0  ;
        BitQ         <= 64'b0  ;
        BitI         <= 64'b0  ;
        flag_E_B     <= 3 'b0  ;
        captura      <= 1'b0   ;
        flag_captura <= 1'b0   ;
        direccion    <= 32'b0  ;
     end
     else begin   
        if(gpo0[23] == 1'b1)begin
            case (gpo0[31:24])
                8'b00000000: o_reset        <= gpo0[0]  ;    //0   
                8'b00000001: reg_i_sw[1:0]  <= gpo0[1:0];    //1 
                8'b00000010: reg_i_sw[3:2]  <= gpo0[1:0];    //2 
                8'b00000011: logeo          <= gpo0[0]  ;    //3
                8'b00000100: begin                           //4 
                             read             <= gpo0[16];   
                             direccion[11:0]  <= gpo0[11:0]; //5
                             end
                8'b00000101: begin                           //6   
                             captura      <= gpo0[0]  ;
                             flag_captura <= captura  ;
                             end
                8'b00000110: flag_E_B      <= gpo0[2:0];     //7
           endcase

            if (salida_captura) begin
                ErrorQ <= o_ErrorQ;
                ErrorI <= o_ErrorI;
                BitQ   <= o_BitQ  ;
                BitI   <= o_BitI  ;
            end
        end
     end
  end 


assign Dato_input      = {8'b0, o_FIRQ, 8'b0, o_FIRI};//Contatenado de las dos salidas del filtro para ser almacenadas en la RAM
assign gpi0            = (read == 1'b1) ? Dato_output  : o_mux_ErrorBits; //Eleccion de la salida de datos
assign o_mux_ErrorBits = (flag_E_B == 3'b000) ? ErrorI[31:0] : (flag_E_B == 3'b001) ? ErrorI[63:32] :
                         (flag_E_B == 3'b010) ? BitI  [31:0] : (flag_E_B == 3'b011) ? BitI  [63:32] : //Bits y errores transmitidos
                         (flag_E_B == 3'b100) ? ErrorQ[31:0] : (flag_E_B == 3'b101) ? ErrorQ[63:32] :
                         (flag_E_B == 3'b110) ? BitQ  [31:0] :  BitQ  [63:32];

assign salida_captura  = ~flag_captura & captura;
assign o_filtroQ       = gpi0[23:16];
assign o_filtroI       = gpi0[7:0];
endmodule

//Register File
//|   0   | ||Reset||
//|   1   | ||Bit 0 Enable PRBS Enable FIR -- Bit 1 Enable Ber||
//|   2   | ||BIT 0 Y 1 FASE||
//|   3   | ||Enable de Logeo||
//|   4   | ||Enable de Lectura de Logeo|| 
//|   5   | ||bit 0 Enable Captura Error y Bits|| 
//|   6   | ||seleccion Error y Bits||

//Error y Bits
//|   000   | ||LEI||
//|   001   | ||HEI||
//|   010   | ||LBI||
//|   011   | ||HBI||
//|   100   | ||LEQ||
//|   101   | ||HEQ||
//|   110   | ||LBQ||
//|   111   | ||HBQ||
