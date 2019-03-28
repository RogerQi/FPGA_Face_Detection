module weight_eval(output [31:0] product, input pixel_val, input [15:0] weight);

    wire [15:0] weight_temp = (pixel_val)? weight : 16'b0;
    wire [31:0] calced_out = {{16{weight_temp[15]}}, weight_temp}; //SEXT

    mux2v #(32) prod_mux(.out(product), .A(32'b0), .B(calced_out), .sel(pixel_val));

endmodule