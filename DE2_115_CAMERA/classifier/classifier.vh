// bbox params
localparam x_min = 320 - 128;
localparam x_max = 320 + 128; //length; should not be accessed
localparam y_min = 240 - 128;
localparam y_max = 240 + 128;  //out-of-bound length; should not be accessed

// localparam max_ind = 1; //(y_max - y_min) * (x_max - x_min)