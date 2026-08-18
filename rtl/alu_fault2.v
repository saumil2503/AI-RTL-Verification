//============================================================
// 4-BIT ALU - FAULT INJECTION VERSION #2
//
// INTENTIONAL FAULT:
// AND operation is incorrectly implemented as OR.
//
// Golden ALU:
// OP = 01  ->  RESULT = A & B
//
// Faulty ALU:
// OP = 01  ->  RESULT = A | B
//
// Purpose:
// Verify that the verification environment can detect
// an incorrect logic implementation.
//============================================================

`timescale 1ns/1ps

module alu_fault2 (

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
            // INTENTIONAL BUG:
            // AND has been replaced with OR.
            //================================================

            2'b01: begin

                RESULT = A | B;

                // Carry remains zero
                CARRY = 1'b0;

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