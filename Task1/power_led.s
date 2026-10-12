@ The GNU Assembler treats the at sign (@) as a single line comment
main:
  ldr   r4, .L1       @ Load the variable from L1 to r4
                      @ NOTE:
                      @ "mov" cannot be used here for 0xFE200000
                      @ which is larger than a 16-bit register
  add   r3, r4, #0x2c @ Calculate the offset for GPCLR1
                      @ and store it in r3
  mov   r2, #0x400    @ Write this value to r2 (you know why ;-))
  str   r2, [r3]      @ Store r2 to the address at r3
.L1:
  .word	0xFE200000    @ GPIO base address
