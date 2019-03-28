module linear_classifier_control_unit(input clock_50,
    output reg classified_result, output reg is_bound,
    input [12:0] true_x, input [12:0] true_y,
    input [9:0] binarized_value, output reg [31:0] frame_sum_holder);

    `include "classifier.vh"

    wire new_frame_mark;
    reg [31:0] current_frame_weight_sum;

    assign new_frame_mark = (true_x == 13'b0000000000001) && (true_y == 13'b0);

    wire y_in_range = (true_y >= y_min) && (true_y < y_max);
    wire x_in_range = (true_x >= x_min) && (true_x < x_max);
    wire [15:0] cur_ind = ((true_y - y_min) * (x_max - x_min));
    wire calc_enable = x_in_range && y_in_range;

    //weight eval reg
    reg pixel_val;
    wire [15:0] weight;
    wire [31:0] product;

    wire is_x_bound, is_y_bound;
    assign is_x_bound = (y_in_range) && ((true_x == x_min) || (true_x == x_max));
    assign is_y_bound = (x_in_range) && ((true_y == y_min) || (true_y == y_max));

    always @ (posedge clock_50) begin
        //these should be combinational logic but we need to synchronize them
        is_bound <= is_x_bound || is_y_bound;
        //be default weight eval should be zero
        pixel_val <= 1'b0;
        //increment weight
        current_frame_weight_sum <= current_frame_weight_sum + product; //note that product is from last rising edge
        if (new_frame_mark) begin
            frame_sum_holder <= current_frame_weight_sum;
            classified_result <= ~(current_frame_weight_sum[31]) && ~(current_frame_weight_sum == 32'b0); //result from last frame
            current_frame_weight_sum <= 32'b0;
        end
        //
        if (calc_enable) begin
            //a valid pixel
            //else weight and pixel would remain unchanged. Thus resulting in a zero
            // weight <= 16'hFFFF; //TODO: change this to get true weight
            pixel_val <= (binarized_value == 10'b1111111111);
        end
    end

    wire [31:0] product_evaled;
    weight_lut twun(.clk(clock_50), .ind(cur_ind), .out(weight));
    weight_eval pixel_eval(.product(product_evaled), .pixel_val(pixel_val), .weight(weight));
    mux2v #(32) weight_valid_mux(.out(product), .A(32'b0), .B(product_evaled), .sel(calc_enable));

endmodule