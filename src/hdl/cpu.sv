`include "alu.sv"
`include "config.sv"
`include "decoder.sv"
`include "memory.sv"
`include "registers.sv"

module cpu (
    input rst,
    input clk
);

// Program counter.
reg [`ADDR_SIZE-1:0] pc;
localparam integer PC_INC = 1;

// Instrucción decodificada.
wire [`INST_SIZE-1:0] inst;
wire [`OPCODE_BITS-1:0] opcode;
wire [`REGISTER_BITS-1:0] idx_rx;
wire [`REGISTER_BITS-1:0] idx_ry;

// Cables para interconectar los componentes.
wire [`WORD_SIZE-1:0] rx;
wire [`WORD_SIZE-1:0] ry;
wire [`WORD_SIZE-1:0] imm;
wire [`WORD_SIZE-1:0] alu_out;
reg flag_c;
reg flag_z;
reg flag_n;
reg carry_in;
wire [`WORD_SIZE-1:0] data_memory_out;
reg [`WORD_SIZE-1:0] registers_data_in;
reg [`REGISTER_BITS-1:0] registers_idx_write;
reg [`WORD_SIZE-1:0] data_memory_data_in;
reg [`ADDR_SIZE-1:0] data_memory_addr;
reg registers_en_write;
reg data_memory_en_write;

// Instruction memory (readonly): contiene las instrucciones del programa en ejecución.
memory #(
    .WORD_SIZE(`INST_SIZE),
    .ADDR_SIZE(`ADDR_SIZE)
) inst_memory (
    .data_out(inst),
    .addr(pc),
    .en_write(1'b0), // Nunca escribimos en la memoria de instrucciones.
    .clk(clk)
);

// Data memory (read/write): contiene los datos del programa.
memory #(
    .WORD_SIZE(`WORD_SIZE),
    .ADDR_SIZE(`ADDR_SIZE)
) data_memory (
    .data_in(data_memory_data_in),
    .data_out(data_memory_out),
    .addr(data_memory_addr),
    .en_write(data_memory_en_write),
    .clk(clk)
);

// Decoder: decodifica la instrucción actual.
decoder decoder (
    .inst(inst),
    .opcode(opcode),
    .rx(idx_rx),
    .ry(idx_ry),
    .imm(imm)
);

// Registers: banco de registros.
registers #(
    .WORD_SIZE(`WORD_SIZE),
    .COUNT(`NUM_REGISTERS)
) registers (
    .data_in(registers_data_in),
    .idx_write(registers_idx_write),
    .en_write(registers_en_write),
    .data_out_a(rx),
    .data_out_b(ry),
    .idx_out_a(idx_rx),
    .idx_out_b(idx_ry),
    .rst(rst),
    .clk(clk)
);

// ALU: hace cuentitas.
alu #(
    .WORD_SIZE(`WORD_SIZE)
) alu (
    .opcode(opcode),
    .a(rx),
    .b(ry),
    .carry_in(carry_in),
    .out(alu_out),
    .flag_c(flag_c),
    .flag_z(flag_z),
    .flag_n(flag_n)
);

// TODO: Qué tipo de always habría que usar acá?
// TODO: Frenar la ejecución si opcode inválido.
always @ (posedge clk or posedge rst) begin
    if (rst) begin
        pc = 0;
        carry_in = 0;
    end else begin
        case (opcode)
            JMP: pc = imm;
            JC: pc = flag_c ? imm : pc + PC_INC;
            JZ: pc = flag_z ? imm : pc + PC_INC;
            JN: pc = flag_n ? imm : pc + PC_INC;
            default: pc = pc + PC_INC;
        endcase
        // TODO: Actualizamos el flag de carry 1 vez por ciclo.
        // Por alguna razón ALU.always_comb se dispara 2 veces por ciclo y se pierde el carry.
        carry_in = flag_c;
    end
end

// Execute: activamos las señales de control y ruteamos los datos según la instrucción.
// Como es un CPU single-cycle, este es un bloque combinatorio.
always_comb begin
    registers_data_in = 0;
    registers_idx_write = 0;
    data_memory_data_in = 0;
    data_memory_addr = 0;
    registers_en_write = 0;
    data_memory_en_write = 0;

    case (opcode)
        // ALU ops
        ADD, ADC, SUB, AND, OR, XOR, CMP, INC, DEC, SHR, SHL: begin
            registers_data_in = alu_out;
            registers_idx_write = idx_rx;
            registers_en_write = 1;
        end

        // Register ops
        MOV: begin // Rx <- Ry
            registers_data_in = ry;
            registers_idx_write = idx_rx;
            registers_en_write = 1;
        end
        SET: begin // Rx <- M
            registers_data_in = imm;
            registers_idx_write = idx_rx;
            registers_en_write = 1;
        end

        // Load/Store ops
        STR: begin // Mem[M] <- Rx
            data_memory_data_in = rx;
            data_memory_addr = imm;
            data_memory_en_write = 1;
        end
        LOAD: begin // Rx <- Mem[M]
            data_memory_addr = imm;
            registers_data_in = data_memory_out;
            registers_idx_write = idx_rx;
            registers_en_write = 1;
        end
        RSTR: begin // Mem[Rx] <- Ry
            data_memory_data_in = ry;
            data_memory_addr = rx;
            data_memory_en_write = 1;
        end
        RLOAD: begin // Rx <- Mem[Ry]
            data_memory_addr = ry;
            registers_data_in = data_memory_out;
            registers_idx_write = idx_rx;
            registers_en_write = 1;
        end
    endcase
end

`ifdef SIM_CPU
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, cpu);
end
`endif

endmodule
