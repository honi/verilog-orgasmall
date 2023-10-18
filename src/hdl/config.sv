`ifndef CONFIG_SV
`define CONFIG_SV

`define WORD_SIZE 8
`define INST_SIZE (`WORD_SIZE * 2)
`define ADDR_SIZE 8
`define OPCODE_BITS 5
`define REGISTER_BITS 3
`define NUM_REGISTERS (1 << `REGISTER_BITS)
`define IMM_BITS 8

typedef enum bit[`OPCODE_BITS-1:0] {
    ADD   = `OPCODE_BITS'b00001, // ADD Rx, Ry
    ADC   = `OPCODE_BITS'b00010, // ADC Rx, Ry
    SUB   = `OPCODE_BITS'b00011, // SUB Rx, Ry
    AND   = `OPCODE_BITS'b00100, // AND Rx, Ry
    OR    = `OPCODE_BITS'b00101, // OR Rx, Ry
    XOR   = `OPCODE_BITS'b00110, // XOR Rx, Ry
    CMP   = `OPCODE_BITS'b00111, // CMP Rx, Ry
    MOV   = `OPCODE_BITS'b01000, // MOV Rx, Ry
    STR   = `OPCODE_BITS'b10000, // STR [M], Rx
    LOAD  = `OPCODE_BITS'b10001, // LOAD Rx, [M]
    RSTR  = `OPCODE_BITS'b10010, // STR [Rx], Ry
    RLOAD = `OPCODE_BITS'b10011, // LOAD Rx, [Ry]
    JMP   = `OPCODE_BITS'b10100, // JMP M
    JC    = `OPCODE_BITS'b10101, // JC M
    JZ    = `OPCODE_BITS'b10110, // JZ M
    JN    = `OPCODE_BITS'b10111, // JN M
    INC   = `OPCODE_BITS'b11000, // INC Rx
    DEC   = `OPCODE_BITS'b11001, // DEC Rx
    SHR   = `OPCODE_BITS'b11010, // SHR Rx, t
    SHL   = `OPCODE_BITS'b11011, // SHL Rx, t
    SET   = `OPCODE_BITS'b11111  // SET Rx, M
} opcode_t;

`endif
