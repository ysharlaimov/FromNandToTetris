// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)


@R2
M=0

// if R1 is 0, end operation
@R1
D=M

@END
D;JEQ

// if R0 is 0, end operation
@R0
D=M

@END
D;JEQ

//init n to R1
@R1
D=M

@n
M=D

// if R1 >0, then start mult loop
// either : negate n
@LOOP
D;JGT

@n
M=-M

(LOOP)
@R0
D=M

@R2
M=M+D

@n
M=M-1

@n
D=M

@LOOP
D;JGT

//negate result if r1 was negative
@R1
D=M

@END
D;JGT

@R3
M=-M

(END)
    @END
    0;JMP
