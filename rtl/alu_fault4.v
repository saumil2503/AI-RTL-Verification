//============================================================
// 4-BIT ALU - FAULT INJECTION VERSION #4
//
// INTENTIONAL FAULT:
// OR operation is incorrectly implemented as XOR.
//
// Golden ALU:
// OP = 10  -> RESULT = A | B
//
// Faulty ALU:
// OP = 10  -> RESULT = A ^ B
//
// Purpose:
// Verify that the verification environment can detect
// an incorrect OR/XOR logic implementation.
//============================================================

`timescale 1ns/1ps

module alu_fault4 (

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
            // INTENTIONAL BUG:
            // OR has been replaced with XOR.
            //================================================

            2'b10: begin

                RESULT = A ^ B;
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