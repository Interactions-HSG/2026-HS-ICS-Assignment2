# Assignment 2 — Report

> **How to use this file.** This file *is* your hand-in. Edit it directly (in Codespaces,
> in your browser, or in any editor) and commit your changes.
>
> Every place you need to write something contains a line starting with `TODO:`.
> Replace that whole line with your answer. When no `TODO:` lines are left, the
> **Submission check** in the Actions tab turns green.
>
> Do not rename this file, and do not delete the `##` / `###` headings — we grade against them.

---

## 0. Team & process

You work in your assigned group of two. Both names go here, whoever created the repository.

| Field | Your entry |
| --- | --- |
| Group number | TODO: |
| Team member 1 (last name, first name) | TODO: |
| Team member 2 (last name, first name) | TODO: |

### 0.1 Roles

Who did what? One or two sentences per person.

TODO: replace this line with your answer.

### 0.2 Pitfalls

What were the major pitfalls you ran into, and how did you get past them?

TODO: replace this line with your answer.

### 0.3 Time spent

Roughly how many hours did this assignment take the two of you in total?

TODO: replace this line with your answer.

### 0.4 AI usage

In this assignment you may use AI for some tasks, and in **Task 2 we ask you to** work together
with one. Which tools did you use, and for what? For Task 2 in particular: how
did you work with it, and was there anything it got wrong that you had to check or correct?

TODO: replace this line with your answer.

---

## 1. Getting Ready (0.5pt)

Assemble [`Task1/power_led.s`](Task1/power_led.s), copy the resulting `kernel7l.img` to your
SD card, and boot the Pi — `make power_led` does the first part for you (see
[`docs/TOOLCHAIN.md`](docs/TOOLCHAIN.md)).

### 1.1 What did you observe?

TODO: replace this line with your answer.

---

## 2. Assembler Forensics (5pt)

> **Work on this task together with an AI assistant or agent:** work out with it what the binary
> does, and debug with it. Check what it tells you against the manual and your Pi. Note how you
> worked with it in section 0.4.

Disassemble [`Task2-3/kernel.elf`](Task2-3/kernel.elf) into `kernel.s` (`make disassemble`).
Wire two LEDs, each with its own 330 Ω resistor:

| LED | GPIO | Physical pin |
| --- | --- | --- |
| LED_0 | BCM 20 | 38 |
| LED_1 | BCM 21 | 40 |

Then run `kernel.elf` on the Pi (`make kernel` produces the `kernel7l.img`) and answer the
questions below.

### 2.1 How do the two LEDs behave? (0.5pt)

How many patterns do you observe, and what do they indicate?

TODO: replace this line with your answer.

### 2.2 Instruction types in `kernel.s` (0.5pt)

How many *types* of instructions do you find in `kernel.s`?

TODO: replace this line with your answer.

List each type with a brief explanation of what it does, based on the
[AArch32 Base Instructions](https://developer.arm.com/documentation/ddi0597/2021-12/Base-Instructions?lang=en)
reference. One per line, for example: `xyz` — what it does.

TODO: replace this line with your list.

### 2.3 Labels and addresses (0.5pt)

Which address in `kernel.s` does each label in [`kernel_clean.s`](Task2-3/kernel_clean.s)
correspond to?

| Label | Address in `kernel.s` |
| --- | --- |
| `.L2` | TODO: |
| `.L3` | TODO: |
| `.L4` | TODO: |
| `.L5` | TODO: |
| `.L6` | TODO: |
| `.L7` | TODO: |
| `.L8` | TODO: |
| `.L9` | TODO: |
| `.L10` | TODO: |

### 2.4 The execution sequence (1pt)

In which order are the instructions actually executed when the program runs? Give each run of
instructions that execute one after another as an address range (e.g. `0x8000` to `0x8yyy`),
and describe where and why the program branches.

TODO: replace this line with your answer.

### 2.5 Switching off both LEDs at once (0.5pt)

Which part of `kernel.s` switches off the two LEDs **at the same time**?

**Address range:**

TODO: e.g. `0x8xxx` to `0x8yyy`

**What happens:** for each instruction in that range, which values are loaded or stored, from
or to where, and how.

TODO: replace this line with your answer.

### 2.6 Loop iterations (1pt)

The intervals between the LED patterns are loops, all with the same number of iterations. How
many iterations does one loop have, and how did you work it out?

TODO: replace this line with your answer.

### 2.7 The original C code (1pt)

Your answer is the code in [`Task2-3/led.c`](Task2-3/led.c) — nothing to write here.
Build it with `make led`.

---

## 3. Tinkering with Instructions (1.5pt)

Your code is [`Task2-3/reverse.s`](Task2-3/reverse.s). It starts as an exact copy of
`kernel_clean.s`; change it so it cycles through the patterns from 2.1 **in reverse order**.
Build it with `make reverse` and run it on the Pi.

### 3.1 Which parts did you modify, and why?

TODO: replace this line with your answer.

---

## 4. Speak Like a Machine (3pt)

### 4.1 The A32 instruction encoding (1.5pt)

What is the A1 encoding of **`ldr r3, [r3]`** (the Offset variant of *LDR (immediate)*) in the
`elf32-littlearm` format?

**The 32-bit instruction word:**

TODO: e.g. `0x........`

**The same instruction as the bytes appear in the file (little-endian):**

TODO: e.g. `.. .. .. ..`

**Each field**, its bits, and what it means according to the manual — like the
`ldr r4, [pc, #8]` example on the assignment sheet:

TODO: replace this line with your answer.

### 4.2 Program counter (PC) and offset (1.5pt)

What is the A1 encoding of **`bcc 0x80e0`** in the `elf32-littlearm` format, if the
instruction is located at the address **`0x810c`**?

**The 32-bit instruction word:**

TODO: e.g. `0x........`

**The same instruction as the bytes appear in the file (little-endian):**

TODO: e.g. `.. .. .. ..`

**Each field**, its bits, and what it means according to the manual:

TODO: replace this line with your answer.

**How you computed `imm24`:**

TODO: replace this line with your answer.

---

## 5. BONUS: The Smaller the Better (up to 3pt)

Make the `kernel7l.img` of [`Bonus/flash.elf`](Bonus/flash.elf) (484 bytes) smaller while
keeping its behaviour. Hand in your optimized program by **replacing `Bonus/flash.elf`** with
it ([`docs/TOOLCHAIN.md`](docs/TOOLCHAIN.md) shows how). `make flash` prints the size. Run the
original on your Pi first, so you know which behaviour to keep.

Points: min(bytes saved × 0.01, 3.0). How similar your program is to the original is judged
individually, so explain your approach in detail.

If you did not attempt the bonus, write `not attempted` below and leave `flash.elf` as it is.

### 5.1 How did you approach it?

What does the original program do, what did you remove or change, and why does the behaviour
stay the same?

TODO: replace this line with your answer.

---

## Before you submit

- [ ] No `TODO:` lines left in this file
- [ ] `Task2-3/led.c` written, and it compiles (`make led`)
- [ ] `Task2-3/reverse.s` modified, and it assembles (`make reverse`)
- [ ] `Bonus/flash.elf` replaced with your optimized version, or section 5.1 says `not attempted`
- [ ] Everything **committed and pushed**
- [ ] Your partner **and** `lukabekavac` **and** `Karimkh31` added as collaborators
- [ ] **One** of you submitted the repository URL on Canvas (not both)
