// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed.
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INF)

@KBD
D=M

@SETWHITE
D;JEQ

@SETBLACK
0;JMP

(SETWHITE)
//32 * 256 - 1
@8191
D=A

@n
M=D

(LOOPW)
@n
D=M

@SCREEN
A=A+D
M=0

@n
M=M-1
D=M

@LOOPW
D;JGE

@INF
0;JMP

(SETBLACK)
//32 * 256 - 1
@8191
D=A

@n
M=D

(LOOPB)
@n
D=M

@SCREEN
A=A+D
M=-1

@n
M=M-1
D=M

@LOOPB
D;JGE

@INF
0;JMP
