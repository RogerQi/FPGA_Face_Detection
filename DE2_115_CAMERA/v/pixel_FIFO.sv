// a pixel FIFO buffer used before vga output to avoid glitches

module pixel_FIFO(
                input logic CLK_1,  // write clock
                input logic CLK_2,  // read clock
                input logic RESET_N,

                input logic [9:0] iRED,
                input logic [9:0] iGREEN,
                input logic [9:0] iBLUE,

                output logic [9:0] oRED,
                output logic [9:0] oGREEN,
                output logic [9:0] oBLUE
            );

logic read;
logic write;

logic empty_RED, empty_GREEN, empty_BLUE;
logic full_RED, full_GREEN, full_BLUE;

logic empty;
logic full;

assign empty = empty_RED && empty_GREEN && empty_BLUE;
assign full = full_RED && full_GREEN && full_BLUE;

assign read = empty ? 1'b0 : 1'b1;
assign write = full ? 1'b0 : 1'b1;

logic [9:0] temp_RED;
logic [9:0] temp_GREEN;
logic [9:0] temp_BLUE;

always_ff @ (posedge CLK_2 or negedge RESET_N)
begin
    if (!RESET_N)
    begin
        oRED <= 10'b0;
        oGREEN <= 10'b0;
        oBLUE <= 10'b0;
    end 
    else 
    begin
        oRED <= temp_RED;
        oGREEN <= temp_GREEN;
        oBLUE <= temp_BLUE;
    end
end

FIFO_Buffer fifo_RED(
                .data(iRED),
                .rdclk(CLK_2),
                .rdreq(read),

                .wrclk(CLK_1),
                .wrreq(write),
                .q(temp_RED),

                .rdempty(empty_RED),
                .wrfull(full_RED)
            );

FIFO_Buffer fifo_GREEN(
                .data(iGREEN),
                .rdclk(CLK_2),
                .rdreq(read),

                .wrclk(CLK_1),
                .wrreq(write),
                .q(temp_GREEN),

                .rdempty(empty_GREEN),
                .wrfull(full_GREEN)
);

FIFO_Buffer fifo_BLUE(
                .data(iBLUE),
                .rdclk(CLK_2),
                .rdreq(read),

                .wrclk(CLK_1),
                .wrreq(write),
                .q(temp_BLUE),

                .rdempty(empty_BLUE),
                .wrfull(full_BLUE)
);

endmodule