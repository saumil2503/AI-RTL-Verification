//============================================================
// 4-BIT ALU - FAULT INJECTION VERSION #6
//
// INTENTIONAL FAULT:
// AND operation uses inverted B instead of B.
//
// Golden behavior:
// OP = 01 -> RESULT = A & B
//
// Faulty behavior:
// OP = 01 -> RESULT = A & ~B
//
// Purpose:
// Verify that the verification environment can detect
// an operand/input-path fault.
//============================================================

`timescale 1ns/1ps

module alu_fault6 (

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
            //
            // INTENTIONAL FAULT:
            // B is inverted before the AND operation.
            //
            // Correct:
            // RESULT = A & B
            //
            // Fault:
            // RESULT = A & ~B
            //================================================

            2'b01: begin

                RESULT = A & ~B;
                CARRY  = 1'b0;

            end


            //================================================
            // OR
            //================================================

            2'b10: begin

                RESULT = A | B;
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