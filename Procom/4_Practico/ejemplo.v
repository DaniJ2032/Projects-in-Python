/*Detector de flancos*/

module examples (

);
    
always @(posedge clock) begin
    
    if(i_reset) begin
        reg_btn     <= 1'b0;     
        reg_modo    <= 1'b0;
    end

    else begin
        reg_btn <= i_btn;

        if(!reg_btn && i_btn) begin
            reg_modo <= ~modo_reg;        
        end    
    end 
end

assign  o_led = (r_sel_fd_sr) ? FS : SR; 

//SELECCION DE COLOR
always @(posedge clock) begin
    
    if(i_reset) begin
        reg_btn     <=  3'b000;
        r_sel_fd_sr <=  1'b0;
        reg_sel_col <=  3'b001;
    end
    
    else begin
        reg_btn <= {i_btn2,i_btn1,i_btn0};

        if(!reg_btn[0] && i_btn[0] && !reg_sel_col[0]) begin
            reg_sel_col <= 3'b001; //en este caso no importa el valor de los otros botones sino miro el boton asignado al color           
                                    //prendo el rojo
        end

        else if(!reg_btn[1] && i_btn[1] && !reg_sel_col[1]) begin
            reg_sel_col <= 3'b010; //en este caso no importa el valor de los otros botones sino miro el boton asignado al color           
                                //prendo el rojo
        end
        else if(!reg_btn[2] && i_btn[2] && !reg_sel_col[2]) begin
            reg_sel_col <= 3'b100; //en este caso no importa el valor de los otros botones sino miro el boton asignado al color           
                            //prendo el rojo    
        end
        else begin
            reg_sel_col <= reg_sel_col;
        end

    end //fin de if principal

end //fin de always   




endmodule