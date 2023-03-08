//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo Contador de BER para el filtro Q 
//
/////////////////////////////////////////////////////////////////////////////////////


module CounterBerQ(
    input               clock       ,    //clock del sistema    
    input               i_reset     ,    //reset del sistema
    input               i_enable    ,    //señal de habilitación del sistema er
    input               i_firQ      ,
    input               i_prbsQ     ,
    input               i_valid     ,    //Dato de validacion del contador

    output              o_FaseSetOkQ,
    output  [63  :0]    ErroresQ    ,
    output  [63  :0]    BitsQ    
    );
    
reg [1023:0] ShiftRegBerQ     ;  //Registro del BER
reg [8   :0] counterDataBerQ  ;  //contador de datos en la BER
reg [10  :0] counterExorQ     ;  //Acumulador a la salida de la exor
reg [9   :0] positionBerQ     ;  //Indica la posicion en la BER
reg [1023:0] posicion_OkQ     ;  //Guarda la posicion óptima
reg [10  :0] auxcountOkQ      ;  //Guarda el minimo valor que se optuvo

reg [63  :0] counterErrQ      ;  //Contador de errores
reg [63  :0] counterBitQ      ;  //Contador de bits 

wire         exorQ            ;  //Operacion de exor
reg          led_faseOkQ      ;  //Registro del Led que indica que se encontro fase óptima 

//________Fase de seteo_____________
always @(posedge clock) begin
    if (i_reset) begin

      ShiftRegBerQ       <= 0;  
      positionBerQ       <= 0;
      counterDataBerQ    <= 0;
      counterExorQ       <= 0;   //Reset de los registros
      led_faseOkQ        <= 0;
      posicion_OkQ       <= 0;
      auxcountOkQ        <= 511;
      counterErrQ        <= 64'b0;
      counterBitQ        <= 64'b0;
      
    end else if (i_enable && ~led_faseOkQ) begin

      counterExorQ <= counterExorQ + exorQ;

      if (i_valid)begin
        counterDataBerQ  <= counterDataBerQ + 1'b1;         //Contador de cada dato entrado en la Ber
        ShiftRegBerQ     <= {ShiftRegBerQ[1022:0],i_prbsQ};  //Entra el dato y se desplaza el registro 
        end

      if (counterDataBerQ == 9'b111111110 && i_valid) begin  //Una vez que llegue a 510 el contador
          counterDataBerQ  <= {9{1'b0}};                     //Reseteamos el contador de datos del BER
          positionBerQ <=  positionBerQ + 1'b1;               //Se incremeta el puntero para recorrer el prox. registro del BER
          
        if(counterDataBerQ == 9'b111111110) begin          

          if (counterExorQ < 1023 && auxcountOkQ == 511)begin //Este if el sistema solo entrara una vez
              auxcountOkQ   <= counterExorQ;                  
              posicion_OkQ  <= positionBerQ;                  //Se almacena el punto donde se obtiene el menor valor
              counterExorQ  <= 0;                            //del contador de Exor y su posición     
        end   
        else counterExorQ   <= 0;                            //Reseteamos el contador de Exor
      
          if(counterExorQ < 1023 )begin                      
            if(counterExorQ < auxcountOkQ ) begin
              auxcountOkQ   <= counterExorQ;                  //En este if se almacena la posicion
              posicion_OkQ  <= positionBerQ;                  //mas óptima y su minimo valor 
              counterExorQ  <= 0;
            end
          end
        end
      end
    if(positionBerQ == 1024 && auxcountOkQ == 0 ) begin
      positionBerQ <= 0; 
    end    
    if(positionBerQ == 0 && auxcountOkQ == 0 )  led_faseOkQ  <= 1'b1; //Si se logro encontrar la fase optima desp.  
  
    end
    ////______Fase se conteo de errores y bits enviados______________
    else begin
        if (led_faseOkQ) begin
          if (i_valid)begin
            counterBitQ  <= counterBitQ + 1'b1;             //Contador de Bits transmitidos
            ShiftRegBerQ <= {ShiftRegBerQ[1022:0],i_prbsQ};  //Entra el dato y se desplaza el registro 
          end   
          if (exorQ == 1) counterErrQ <= counterErrQ + 1'b1; //contador de errores
        end
    end                  
end


assign o_FaseSetOkQ = led_faseOkQ;
assign exorQ        = (~led_faseOkQ) ? (i_firQ  ^ ShiftRegBerQ[positionBerQ]) : (i_firQ  ^ ShiftRegBerQ[posicion_OkQ]); 
assign ErroresQ     = counterErrQ;
assign BitsQ        = counterBitQ;
endmodule
