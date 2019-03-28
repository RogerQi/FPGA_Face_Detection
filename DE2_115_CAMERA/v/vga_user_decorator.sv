// user added decorator between FIFO buffer and final vga output 

module vga_user_decorator(
                            // control signals
                            input logic iCLK,
                            input logic iCLK_50, 
                            input logic iRST_N,
                            input logic [17:0] iSW,

                            // image (pixel) signals
                            input logic [12:0] iX_POS,
                            input logic [12:0] iY_POS,

                            input logic [9:0] iRED,
                            input logic [9:0] iGREEN,
                            input logic [9:0] iBLUE,

                            // outputs
                            output logic [9:0] oRED,
                            output logic [9:0] oGREEN,
                            output logic [9:0] oBLUE,

                            // debug outputs
                            output logic oClassifiedResult,
                            output logic [31:0] oCFWS
                        );

//================= some interesting filters for tests ==================

// gray scale and binarization
logic [10:0] gray_scale_temp;
logic [9:0] gray_scale;
logic [9:0] binarized;

assign gray_scale_temp = (iRED + iGREEN + iBLUE);
assign gray_scale = {1'b0, gray_scale_temp[10:2]};

always_ff @ (posedge iCLK_50)
begin
    binarized <= (gray_scale[9:2] > 8'd25)? 10'b1111111111 : 10'b0;
end

// gray scale and binarization

//======================= end interesting filters =======================

//======================= add Roger's magic here =============================

logic is_bound;

linear_classifier_control_unit lccu (
                                .clock_50(iCLK),
                                .classified_result(oClassifiedResult),
                                .is_bound(is_bound),
                                .true_x(iX_POS),
                                .true_y(iY_POS),
                                .binarized_value(binarized),
                                .frame_sum_holder(oCFWS)
                                );

//============================================================================

//======================= switch logic =======================
logic [17:0] mSW;

always_ff @ (posedge iCLK_50 or negedge iRST_N)
begin
    if (!iRST_N)
        mSW <= 18'b0;
    else
        mSW <= iSW;
end

always_comb
begin
    case (mSW) 
        18'b100000000000000000: begin
        // gray scale
            oRED = gray_scale;
            oGREEN = gray_scale;
            oBLUE = gray_scale;
        end

        18'b010000000000000000: begin
        // binarization
            oRED = binarized;
            oGREEN = binarized;
            oBLUE = binarized;
        end

        18'b001000000000000000: begin
        // draw bbox 
            if (is_bound) begin
                if (oClassifiedResult) begin
                    oRED = 10'hFFF;
                    oGREEN = 10'b0;
                    oBLUE = 10'b0;
                end else begin
                    oRED = 10'b0;
                    oGREEN = 10'hFFF;
                    oBLUE = 10'b0;
                end
            end else begin
                oRED = iRED;
                oGREEN = iGREEN;
                oBLUE = iBLUE;
            end
        end

        18'b011000000000000000: begin
        // draw bbox 
            if (is_bound) begin
                if (oClassifiedResult) begin
                    oRED = 10'hFFF;
                    oGREEN = 10'b0;
                    oBLUE = 10'b0;
                end else begin
                    oRED = 10'b0;
                    oGREEN = 10'hFFF;
                    oBLUE = 10'b0;
                end
            end else begin
                oRED = binarized;
                oGREEN = binarized;
                oBLUE = binarized;
            end
        end

        // TO-DO: add other functionalities

        default: begin
            oRED = iRED;
            oGREEN = iGREEN;
            oBLUE = iBLUE;
        end 
    endcase
end
//======================= end switch logic =======================

endmodule