@ reverse.s -- Task 3: cycle through the LED patterns IN REVERSE ORDER
@
@ This file starts out as an exact copy of kernel_clean.s, which shows the patterns
@ you described in Task 2.1 in their original order. Your job is to change it so it
@ shows the same patterns in the opposite order. Leave kernel_clean.s as it is.
@
@ Explain what you changed, and why, in section 3 of REPORT.md.
@
@ Build it with:   make reverse        (produces kernel7l.img)

main:
    movw	r2, #33252	@ 0x81e4
    movt	r2, #1
    mov		r3, #0
    movt	r3, #65056	@ 0xfe20
    str		r3, [r2]
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #8
    ldr		r2, [r3]
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #8
    orr		r2, r2, #9
    str		r2, [r3]
.L10:
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #40	@ 0x28
    mov		r2, #3145728	@ 0x300000
    str		r2, [r3]
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    mov		r2, #0
    str		r2, [r3]
    b		.L2
.L3:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    add		r2, r3, #1
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    str		r2, [r3]
.L2:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    cmp		r3, #983040	@ 0xf0000
    bcc		.L3
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #28
    mov		r2, #1048576	@ 0x100000
    str		r2, [r3]
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #40	@ 0x28
    mov		r2, #2097152	@ 0x200000
    str		r2, [r3]
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    mov		r2, #0
    str		r2, [r3]
    b		.L4
.L5:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    add		r2, r3, #1
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    str		r2, [r3]
.L4:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    cmp		r3, #983040	@ 0xf0000
    bcc		.L5
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #40	@ 0x28
    mov		r2, #1048576	@ 0x100000
    str		r2, [r3]
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #28
    mov		r2, #2097152	@ 0x200000
    str		r2, [r3]
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    mov		r2, #0
    str		r2, [r3]
    b		.L6
.L7:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    add		r2, r3, #1
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    str		r2, [r3]
.L6:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    cmp		r3, #983040	@ 0xf0000
    bcc		.L7
    movw	r3, #33252	@ 0x81e4
    movt	r3, #1
    ldr		r3, [r3]
    add		r3, r3, #28
    mov		r2, #3145728	@ 0x300000
    str		r2, [r3]
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    mov		r2, #0
    str		r2, [r3]
    b		.L8
.L9:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    add		r2, r3, #1
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    str		r2, [r3]
.L8:
    movw	r3, #33256	@ 0x81e8
    movt	r3, #1
    ldr		r3, [r3]
    cmp		r3, #983040	@ 0xf0000
    bcc		.L9
    b		.L10
