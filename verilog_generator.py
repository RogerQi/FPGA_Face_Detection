import os
import numpy as np
import perceptron_config
from IPython import embed

weight_mat_width = perceptron_config.weight_mat_width
weight_mat_height = perceptron_config.weight_mat_height

input_bytes = 16
output_bytes = 16 #signed int16

#TODO: modify this to real weight mat from trained weight matrix
weight_mat = np.ones(2**input_bytes) #bias weight is implemented directly in SV
weight_mat[:2**(input_bytes - 1)] = -1 #upper half weights are set to -1
weight_mat = np.array(weight_mat, dtype = "int16")

stupid_lut = {'0':'1', '1':'0'}

#roughly tested
def get_two_comp_bin(number, total_byte_count):
    bin_rep_str = bin(abs(number))[2:]
    if number < 0:
        #negative, flip bit
        ori_len = len(bin_rep_str)
        temp = [stupid_lut[i] for i in list(bin_rep_str)] #flip bit
        bin_rep_str = ''.join(temp)
        #add 1
        bin_rep = int(bin_rep_str, 2) + 1
        bin_rep = bin(bin_rep)[2:]
        while len(bin_rep) < ori_len:
            bin_rep = '0' + bin_rep
        bin_rep_str = '1' + bin_rep
    else:
        bin_rep_str = '0' + bin_rep_str
    #sext or cut
    cur_len = len(bin_rep_str)
    while cur_len < total_byte_count:
        bin_rep_str = bin_rep_str[0] + bin_rep_str
        cur_len += 1
    if (cur_len > total_byte_count):
        bin_rep_str = bin_rep_str[-output_bytes:]
    return bin_rep_str

def get_two_comp_hex(number, total_byte_count = output_bytes):
    two_comp_bin_rep = get_two_comp_bin(number, total_byte_count)
    assert len(two_comp_bin_rep) % 4 == 0
    ret = []
    for i in range(0, len(two_comp_bin_rep), 4):
        ret.append(hex(int(two_comp_bin_rep[i:i + 4], 2)).upper()[2])
    return ''.join(ret)

def make_title():
    print("module weight_lut (input logic clk, input logic [{0}:0] ind, output logic [{1}:0] out);\n".format(input_bytes - 1, output_bytes - 1))

def make_main_lut(weight_mat):
    #weight mat is 1d
    lut_str = "    {0}'d{2}: out <= {1}'h{6};    {0}'d{3}: out <= {1}'h{7};    {0}'d{4}: out <= {1}'h{8};    {0}'d{5}: out <= {1}'h{9};"
    #assert(len(weight_mat) == 2**input_bytes)
    print("always_ff @ (negedge clk)")
    print("    case(ind)")
    for i in range(0, len(weight_mat), 4):
        #embed()
        a, b, c, d = [get_two_comp_hex(i) for i in weight_mat[i:i+4]]
        print(lut_str.format(input_bytes, output_bytes, i, i + 1, i + 2, i + 3, a, b, c, d))

def make_end():
    print("    default: out <= {0}'h{1};".format(output_bytes, get_two_comp_hex(0)))
    print("    endcase")
    print("endmodule")

def main(weight_mat = weight_mat):
    make_title()
    make_main_lut(weight_mat)
    make_end()

if __name__ == '__main__':
    main()