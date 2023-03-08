module counter(
        input  clock    ,
        input  i_enable ,
        input  i_reset    ,
        // output [2:0] o_counter,
        output o_valid
    );
    
    reg [2:0] counter_reg;
    reg       valid;
     
    always @(posedge clock) begin
        if (i_reset == 1'b1) begin
            counter_reg <= 2'b00;
            valid   <= 1'b0;
        end
        else if (i_enable == 1'b1)begin

            if (counter_reg <= 2'b11) begin
                counter_reg <= counter_reg + 2'b01;
                valid <= 1'b0;
            end    
            else begin
                counter_reg <= 2'b00;
                valid <= 1'b1;
            end    
        end
        else begin
            counter_reg <= counter_reg;
            valid <= valid;
        end    
    end
    // assign counter = counter_reg; 
    assign o_valid = valid      ;      
endmodule
