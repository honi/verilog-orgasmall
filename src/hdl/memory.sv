`include "config.sv"

module memory #(
    parameter longint WORD_SIZE = `WORD_SIZE,
    parameter longint ADDR_SIZE = `ADDR_SIZE,
    localparam longint MAX_ADDR = (1 << ADDR_SIZE) - 1
)(
    input [WORD_SIZE-1:0] data_in,
    output [WORD_SIZE-1:0] data_out,
    input [ADDR_SIZE-1:0] addr,
    input en_write,
    input rst,
    input clk
);

reg [WORD_SIZE-1:0] data [0:MAX_ADDR];

always_ff @ (posedge clk or posedge rst) begin
    longint i;
    if (rst) begin
        for (i = 0; i <= MAX_ADDR; i = i + 1) begin
            data[i] <= '0;
        end
    end else begin
        if (en_write) data[addr] <= data_in;
    end
end

assign data_out = data[addr];

`ifdef COCOTB_SIM
initial begin
    $dumpfile("memory.vcd");
    $dumpvars(0, memory);
end
`endif

endmodule
