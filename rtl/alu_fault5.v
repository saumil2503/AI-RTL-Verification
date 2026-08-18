//============================================================
// 4-BIT ALU - FAULT INJECTION VERSION #5
//
// INTENTIONAL FAULT:
// Opcode 10 is incorrectly mapped to AND instead of OR.
//
// Correct opcode mapping:
//
// OP = 00 -> ADD
// OP = 01 -> AND
// OP = 10 -> OR
// OP = 11 -> XOR
//
// Faulty opcode mapping:
//
// OP = 10 -> AND   <-- INTENTIONAL BUG
//
// Purpose:
// Verify that the verification environment can detect
// an opcode/control-selection fault.
//============================================================

`timescale 1ns/1ps

module alu_fault5 (

    input  [3:0] A,
    input  [3:0] B,
    input  [1:0] OP,

    output reg [3:0] RESULT,
    output reg       CARRY

);

    always @(*) begin

        // Default values
        RESULT = 4'b0000;
        CARRY  = 1'b0;

        case (OP)

            //================================================
            // ADD
            //================================================

            2'b00: begin

                {CARRY, RESULT} = A + B;

            end


            //================================================
            // AND
            //================================================

            2'b01: begin

                RESULT = A & B;
                CARRY  = 1'b0;

            end


            //================================================
            // OR
            //
            // INTENTIONAL OPCODE FAULT:
            //
            // OP = 10 should perform OR.
            // Instead, it performs AND.
            //================================================

            2'b10: begin

                RESULT = A & B;
                CARRY  = 1'b0;

            end


            //================================================
            // XOR
            //================================================

            2'b11: begin

                RESULT = A ^ B;
                CARRY  = 1'b0;

            end


            //================================================
            // DEFAULT
            //================================================

            default: begin

                RESULT = 4'b0000;
                CARRY  = 1'b0;

            end

        endcase

    end

endmodule