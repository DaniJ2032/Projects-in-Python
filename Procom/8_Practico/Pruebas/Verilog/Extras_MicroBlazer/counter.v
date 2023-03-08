//////////////////////////////////////////////////////////////////////////////////
// AUTOR: Jose gomez Lazarte, Juarez Daniel 
// AÑO:   2023  
// NOMBRE: Módulo Counter para habilitacion de datos del modulo PRBS 
//
//////////////////////////////////////////////////////////////////////////////////

module counter(
    
        input  clock,
        input  i_reset,        
        input  i_enable,
        output [2:0] o_counter_mux,
        output o_validPrbs
    );
    

    reg [2:0] counter_reg_prbs;   //contador de 4 bits 
    reg       validPrbs; // --> 24

    always @(posedge clock) begin
        if (i_reset) begin
            counter_reg_prbs    <= 2'b00;
            validPrbs           <= 1'b0 ;
        end

        else if (i_enable == 1'b1)begin
            
            if (counter_reg_prbs < 2'b11) begin     //Menor a 4
                counter_reg_prbs <= counter_reg_prbs + 2'b01;
                validPrbs <= 1'b0;
            end    
                else begin
                    counter_reg_prbs <= counter_reg_prbs;
                    validPrbs <= 1'b1;                  //Habilito la prbs
                    counter_reg_prbs <= 2'b00;
                end    
        end
        else begin
            counter_reg_prbs    <= counter_reg_prbs;
            validPrbs           <= validPrbs;
        end    
    end

    assign o_counter_mux = counter_reg_prbs; 
    assign o_validPrbs   = validPrbs;  

endmodule
