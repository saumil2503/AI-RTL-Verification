//============================================================
// 4-BIT ALU - FAULT INJECTION VERSION #1
//
// INTENTIONAL FAULT:
// ADD operation does not generate carry.
//
// Golden ALU:
// {CARRY, RESULT} = A + B
//
// Faulty ALU:
// RESULT = A + B
// CARRY  = 0
//
// Purpose:
// Verify that the verification environment detects
// an RTL implementation bug.
//============================================================

`timescale 1ns/1ps

module alu_faulty (

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
            //
            // INTENTIONAL BUG:
            // Carry output is forced to zero.
            //================================================

            2'b00: begin

                RESULT = A + B;

                // BUG:
                // CARRY should contain the overflow bit.
                CARRY = 1'b0;

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