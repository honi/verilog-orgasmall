module memory #(
    // TODO: Tipos usados para los parámetros limitan las opciones de configuración?
    parameter longint WORD_SIZE = 16,
    parameter longint ADDR_SIZE = 16,
    localparam longint MAX_ADDR = (1 << ADDR_SIZE) - 1
)(
    input [WORD_SIZE-1:0] data_in,
    output reg [WORD_SIZE-1:0] data_out,
    input [ADDR_SIZE-1:0] addr,
    input we, // write enable
    input oe, // output enable
    input rst,
    input clk
);

reg [WORD_SIZE-1:0] ram [0:MAX_ADDR];

always_ff @ (posedge clk or posedge rst) begin
    longint i;
    if (rst) begin
        for (i = 0; i < MAX_ADDR; i = i + 1) begin
            ram[i] <= '0;
        end
        data_out <= 'z;
    end else begin
        if (we) ram[addr] <= data_in;
        data_out <= (oe & !we) ? ram[addr] : 'z;
    end
end

`ifdef COCOTB_SIM
initial begin
    $display("WORD_SIZE = %0d bits", WORD_SIZE);
    $display("ADDR_SIZE = %0d bits", ADDR_SIZE);
    $display("MAX_ADDR = 0x%0h", MAX_ADDR);
    $dumpfile("dump.vcd");
    $dumpvars(0, memory);
end
`endif

endmodule
