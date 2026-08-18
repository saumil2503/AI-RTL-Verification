`timescale 1ns/1ps

//======================================================================
// AI-ASSISTED RTL VERIFICATION
// 4-BIT ALU - COMPLETE FAULT DATASET GENERATOR
//
// Generates:
//      6 Faults
//      32 Behavioral Windows
//      32 Vectors / Window
//      6144 total verification rows
//
// CSV FORMAT:
//
// fault_id,A,B,OP,expected_result,expected_carry,
// actual_result,actual_carry,result_error,carry_error,bit_errors
//
// Fault mapping:
//
// Fault #1 -> alu_faulty  : ADD Carry Fault
// Fault #2 -> alu_fault2  : AND -> OR
// Fault #3 -> alu_fault3  : XOR -> XNOR
// Fault #4 -> alu_fault4  : OR -> XOR
// Fault #5 -> alu_fault5  : Opcode Selection Fault
// Fault #6 -> alu_fault6  : Inverted B Operand Fault
//======================================================================

module new_verification_tb;

    //============================================================
    // DUT INPUTS
    //============================================================

    reg [3:0] A;
    reg [3:0] B;
    reg [1:0] OP;

    //============================================================
    // EXPECTED GOLDEN OUTPUT
    //============================================================

    reg [3:0] expected_result;
    reg       expected_carry;

    //============================================================
    // FAULTY ALU OUTPUTS
    //============================================================

    wire [3:0] result1;
    wire       carry1;

    wire [3:0] result2;
    wire       carry2;

    wire [3:0] result3;
    wire       carry3;

    wire [3:0] result4;
    wire       carry4;

    wire [3:0] result5;
    wire       carry5;

    wire [3:0] result6;
    wire       carry6;

    //============================================================
    // CSV FILE
    //============================================================

    integer csv_file;

    //============================================================
    // LOOP VARIABLES
    //============================================================

    integer window_id;
    integer vector_id;

    //============================================================
    // TEMPORARY ERROR VARIABLES
    //============================================================

    integer result_error;
    integer carry_error;
    integer bit_errors;

    //============================================================
    // TEMPORARY VECTOR GENERATION
    //============================================================

    integer vector_number;

    //============================================================
    // FAULT #1
    //
    // IMPORTANT:
    // Fault #1 module is alu_faulty
    //============================================================

    alu_faulty U1 (
        .A      (A),
        .B      (B),
        .OP     (OP),
        .RESULT (result1),
        .CARRY  (carry1)
    );

    //============================================================
    // FAULT #2
    //============================================================

    alu_fault2 U2 (
        .A      (A),
        .B      (B),
        .OP     (OP),
        .RESULT (result2),
        .CARRY  (carry2)
    );

    //============================================================
    // FAULT #3
    //============================================================

    alu_fault3 U3 (
        .A      (A),
        .B      (B),
        .OP     (OP),
        .RESULT (result3),
        .CARRY  (carry3)
    );

    //============================================================
    // FAULT #4
    //============================================================

    alu_fault4 U4 (
        .A      (A),
        .B      (B),
        .OP     (OP),
        .RESULT (result4),
        .CARRY  (carry4)
    );

    //============================================================
    // FAULT #5
    //============================================================

    alu_fault5 U5 (
        .A      (A),
        .B      (B),
        .OP     (OP),
        .RESULT (result5),
        .CARRY  (carry5)
    );

    //============================================================
    // FAULT #6
    //============================================================

    alu_fault6 U6 (
        .A      (A),
        .B      (B),
        .OP     (OP),
        .RESULT (result6),
        .CARRY  (carry6)
    );

    //============================================================
    // FUNCTION: COUNT BIT DIFFERENCES
    //
    // Compares two 4-bit values.
    //
    // Example:
    //
    // expected = 1010
    // actual   = 1110
    //
    // difference = 0100
    //
    // bit_errors = 1
    //============================================================

    function integer count_bit_errors;

        input [3:0] expected_value;
        input [3:0] actual_value;

        integer i;
        integer count;

        begin

            count = 0;

            for (i = 0; i < 4; i = i + 1)
            begin

                if (expected_value[i] != actual_value[i])
                    count = count + 1;

            end

            count_bit_errors = count;

        end

    endfunction


    //============================================================
    // GOLDEN ALU
    //
    // OP:
    //
    // 00 -> ADD
    // 01 -> AND
    // 10 -> OR
    // 11 -> XOR
    //============================================================

    task calculate_expected;

        begin

            expected_result = 4'b0000;
            expected_carry  = 1'b0;

            case (OP)

                2'b00:
                begin

                    expected_result = A + B;

                    if ((A + B) > 15)
                        expected_carry = 1'b1;
                    else
                        expected_carry = 1'b0;

                end

                2'b01:
                begin

                    expected_result = A & B;
                    expected_carry  = 1'b0;

                end

                2'b10:
                begin

                    expected_result = A | B;
                    expected_carry  = 1'b0;

                end

                2'b11:
                begin

                    expected_result = A ^ B;
                    expected_carry  = 1'b0;

                end

            endcase

        end

    endtask


    //============================================================
    // TASK: WRITE ONE CSV ROW
    //============================================================

    task write_fault_row;

        input integer fault_number;
        input [3:0] actual_result_value;
        input       actual_carry_value;

        begin

            // Result mismatch
            if (actual_result_value != expected_result)
                result_error = 1;
            else
                result_error = 0;

            // Carry mismatch
            if (actual_carry_value != expected_carry)
                carry_error = 1;
            else
                carry_error = 0;

            // Number of incorrect result bits
            bit_errors =
                count_bit_errors(
                    expected_result,
                    actual_result_value
                );

            // CSV row
            $fwrite(
                csv_file,
                "%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d,%0d\n",
                fault_number,
                A,
                B,
                OP,
                expected_result,
                expected_carry,
                actual_result_value,
                actual_carry_value,
                result_error,
                carry_error,
                bit_errors
            );

        end

    endtask


    //============================================================
    // GENERATE TEST VECTOR
    //
    // 32 vectors per behavioral window.
    //
    // Every window contains:
    //
    // 8 ADD
    // 8 AND
    // 8 OR
    // 8 XOR
    //
    // Therefore:
    //
    // 32 vectors/window
    // 32 windows/fault
    // 6 faults
    //
    // = 6144 rows
    //============================================================

    task generate_vector;

        input integer w;
        input integer v;

        integer base_value;

        begin

            // ---------------------------------------------------
            // Operation
            //
            // 0-7   -> ADD
            // 8-15  -> AND
            // 16-23 -> OR
            // 24-31 -> XOR
            // ---------------------------------------------------

            if (v < 8)
                OP = 2'b00;

            else if (v < 16)
                OP = 2'b01;

            else if (v < 24)
                OP = 2'b10;

            else
                OP = 2'b11;


            // ---------------------------------------------------
            // Deterministic stimulus generation
            //
            // Window 0 / Vector 0 starts with:
            //
            // A = 0
            // B = 0
            // OP = 0
            //
            // This preserves the same initial structure as the
            // existing dataset.
            // ---------------------------------------------------

            base_value = (w * 32) + v;


            // A cycles through 0-F
            A = base_value % 16;

            // B uses a different deterministic pattern
            B = ((base_value * 3) + w) % 16;


            // ---------------------------------------------------
            // Force first vector to the known initial condition
            // ---------------------------------------------------

            if ((w == 0) && (v == 0))
            begin

                A  = 4'd0;
                B  = 4'd0;
                OP = 2'b00;

            end

        end

    endtask


    //============================================================
    // MAIN TEST
    //============================================================

    initial
    begin

        // -------------------------------------------------------
        // Initialize
        // -------------------------------------------------------

        A = 4'b0000;
        B = 4'b0000;
        OP = 2'b00;

        expected_result = 4'b0000;
        expected_carry  = 1'b0;


        // -------------------------------------------------------
        // Open CSV
        // -------------------------------------------------------

        csv_file = $fopen(
            "C:/Users/psaum/OneDrive/Desktop/AI_RTL_Verification/dataset/fault_dataset.csv",
            "w"
        );


        if (csv_file == 0)
        begin

            $display("");
            $display("ERROR: Could not open fault_dataset.csv");
            $display("");

            $finish;

        end


        // -------------------------------------------------------
        // CSV HEADER
        // -------------------------------------------------------

        $fwrite(
            csv_file,
            "fault_id,A,B,OP,expected_result,expected_carry,actual_result,actual_carry,result_error,carry_error,bit_errors\n"
        );


        // -------------------------------------------------------
        // MAIN DATASET GENERATION
        // -------------------------------------------------------

        for (window_id = 0;
             window_id < 32;
             window_id = window_id + 1)
        begin

            $display("");
            $display(
                "================================================"
            );

            $display(
                "GENERATING BEHAVIORAL WINDOW %0d / 31",
                window_id
            );

            $display(
                "================================================"
            );


            for (vector_id = 0;
                 vector_id < 32;
                 vector_id = vector_id + 1)
            begin

                // Generate A/B/OP
                generate_vector(
                    window_id,
                    vector_id
                );

                // Calculate golden expected output
                calculate_expected();

                // Allow combinational DUTs to settle
                #1;


                // ------------------------------------------------
                // Fault #1
                // alu_faulty
                // ------------------------------------------------

                write_fault_row(
                    1,
                    result1,
                    carry1
                );


                // ------------------------------------------------
                // Fault #2
                // ------------------------------------------------

                write_fault_row(
                    2,
                    result2,
                    carry2
                );


                // ------------------------------------------------
                // Fault #3
                // ------------------------------------------------

                write_fault_row(
                    3,
                    result3,
                    carry3
                );


                // ------------------------------------------------
                // Fault #4
                // ------------------------------------------------

                write_fault_row(
                    4,
                    result4,
                    carry4
                );


                // ------------------------------------------------
                // Fault #5
                // ------------------------------------------------

                write_fault_row(
                    5,
                    result5,
                    carry5
                );


                // ------------------------------------------------
                // Fault #6
                // ------------------------------------------------

                write_fault_row(
                    6,
                    result6,
                    carry6
                );


                // Small delay between vectors
                #1;

            end

        end


        // -------------------------------------------------------
        // CLOSE CSV
        // -------------------------------------------------------

        $fclose(csv_file);


        // -------------------------------------------------------
        // FINAL MESSAGE
        // -------------------------------------------------------

        $display("");
        $display("");
        $display("============================================================");
        $display("        AI RTL VERIFICATION DATASET COMPLETE");
        $display("============================================================");

        $display("");
        $display("Fault classes       : 6");
        $display("Behavioral windows  : 32");
        $display("Vectors / window    : 32");
        $display("Vectors / fault     : 1024");
        $display("Total CSV rows      : 6144");

        $display("");
        $display(
            "CSV generated at:"
        );

        $display(
            "dataset/fault_dataset.csv"
        );

        $display("");
        $display("============================================================");
        $display("             VIVADO -> AI PIPELINE READY");
        $display("============================================================");

        $display("");

        #10;

        $finish;

    end

endmodule