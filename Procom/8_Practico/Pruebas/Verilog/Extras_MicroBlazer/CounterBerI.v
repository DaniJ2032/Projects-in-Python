//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo Contador de BER para el filtro I 
//
/////////////////////////////////////////////////////////////////////////////////////


module CounterBerI(
    input               clock       ,    //clock del sistema    
    input               i_reset     ,    //reset del sistema
    input               i_enable    ,    //señal de habilitación del sistema 
    input               i_firI      ,    //Entrada de datos de la salida del Slicer
    input               i_prbsI     ,    //Entrada de datos proveniente de la PRBS
    input               i_valid     ,    //Dato de validacion del contador

    output              o_FaseSetOkI,    //Salida del mínimo error
    output  [63  :0]    ErroresI    ,
    output  [63  :0]    BitsI
    );
    
reg [1023:0] ShiftRegBerI   ;  //Registro del BER
reg [8   :0] counterDataBerI;  //contador de datos en la BER
reg [10  :0] counterExorI   ;  //Acumulador a la salida de la exor
reg [9   :0] positionBerI   ;  //Indica la posicion en la BER
reg [1023:0] posicion_OkI   ;  //Guarda la posicion óptima
reg [10  :0] auxcountOkI    ;  //Guarda el minimo valor que se optuvo

reg [63  :0] counterErrI      ;  //Contador de errores
reg [63  :0] counterBitI      ;  //Contador de bits 

wire         exorI            ;  //Operacion de exor
reg          led_faseOkI      ;  //Registro del Led que indica que se encontro fase óptima 

//________Fase de seteo_____________
always @(posedge clock) begin
    if (i_reset) begin

      ShiftRegBerI       <= 0;  
      positionBerI       <= 0;
      counterDataBerI    <= 0;
      counterExorI       <= 0;   //Reset de los registros
      led_faseOkI        <= 0;
      posicion_OkI       <= 0;
      auxcountOkI        <= 511;
      counterErrI        <= 64'b0;
      counterBitI        <= 64'b0;
      
    end else if (i_enable && ~led_faseOkI) begin

      counterExorI <= counterExorI + exorI;

      if (i_valid)begin
        counterDataBerI  <= counterDataBerI + 1'b1;         //Contador de cada dato entrado en la Ber
        ShiftRegBerI     <= {ShiftRegBerI[1022:0],i_prbsI};  //Entra el dato y se desplaza el registro 
        end

      if (counterDataBerI == 9'b111111110 && i_valid) begin  //Una vez que llegue a 510 el contador
          counterDataBerI  <= {9{1'b0}};                     //Reseteamos el contador de datos del BER
          positionBerI <=  positionBerI + 1'b1;               //Se incremeta el puntero para recorrer el prox. registro del BER
          
        if(counterDataBerI == 9'b111111110) begin          

          if (counterExorI < 1023 && auxcountOkI == 511)begin //Este if el sistema solo entrara una vez
              auxcountOkI   <= counterExorI;                  
              posicion_OkI  <= positionBerI;                  //Se almacena el punto donde se obtiene el menor valor
              counterExorI  <= 0;                            //del contador de Exor y su posición     
        end   
        else counterExorI   <= 0;                            //Reseteamos el contador de Exor
      
          if(counterExorI < 1023 )begin                      
            if(counterExorI < auxcountOkI ) begin
              auxcountOkI   <= counterExorI;                  //En este if se almacena la posicion
              posicion_OkI  <= positionBerI;                  //mas óptima y su minimo valor 
              counterExorI  <= 0;
            end
          end
        end
      end
    if(positionBerI == 1024 && auxcountOkI == 0 ) begin
      positionBerI <= 0; 
    end    
    if(positionBerI == 0 && auxcountOkI == 0 )  led_faseOkI  <= 1'b1; //Si se logro encontrar la fase optima desp.  
  
    end
    ////______Fase se conteo de errores y bits enviados______________
    else begin
       if (led_faseOkI) begin
          if (i_valid)begin
            counterBitI  <= counterBitI + 1'b1;             //Contador de Bits transmitidos
            ShiftRegBerI <= {ShiftRegBerI[1022:0],i_prbsI};  //Entra el dato y se desplaza el registro 
          end   
       if (exorI == 1) counterErrI <= counterErrI + 1'b1; //contador de errores
       end
    end                   
end


assign o_FaseSetOkI = led_faseOkI;
assign exorI        = (~led_faseOkI) ? (i_firI  ^ ShiftRegBerI[positionBerI]) : (i_firI  ^ ShiftRegBerI[posicion_OkI]); 
assign ErroresI     = counterErrI;
assign BitsI        = counterBitI;
endmodule
