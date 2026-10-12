# Toolchain, commands, and the SD card

Every command you need for this assignment, task by task. Come back here whenever the sheet
says "see `docs/TOOLCHAIN.md`".

*(New here? Read the [README](../README.md) first — it covers getting your copy of the
repository.)*

---

## 1. Your toolchain

You installed the ARM GNU toolchain in Assignment 1 — this assignment uses the same one. Besides
the compiler, it contains the two tools that are the stars of this assignment:

| Tool | What it does |
| --- | --- |
| `arm-none-eabi-as` | the **assembler**: turns assembly code (`.s`) into machine code |
| `arm-none-eabi-objdump` | the **disassembler**: turns machine code back into readable assembly |
| `arm-none-eabi-objcopy` | strips the ELF wrapper, leaving the raw image the Pi boots |

Check that they work:

```console
arm-none-eabi-as --version
arm-none-eabi-objdump --version
```

If you get **"command not found"**, the toolchain is not on your PATH (or not installed on this
machine). Follow
[Assignment 1's toolchain guide](https://github.com/Interactions-HSG/2026-HS-ICS-Assignment1/blob/main/docs/TOOLCHAIN.md)
again, then open a **brand-new terminal window**.

---

## 2. The SD card

Use the same SD card as in Assignment 1. It still needs `config.txt`, `fixup4.dat` and
`start4.elf` at its top level — if you lost them, they are in [`boot/`](../boot/) here too.

For every task you only replace one file on the card: **`kernel7l.img`**. Copy it over, eject
the card properly, put it in the Pi, and plug in the power.

---

## 3. Building — the short way

From the main folder of your repository:

```console
make power_led         # Task 1   -- assemble Task1/power_led.s
make kernel            # Task 2   -- the given Task2-3/kernel.elf
make disassemble       # Task 2   -- disassemble kernel.elf into Task2-3/kernel.s
make led               # Task 2.7 -- compile your Task2-3/led.c
make reverse           # Task 3   -- assemble your Task2-3/reverse.s
make flash             # Bonus    -- the given Bonus/flash.elf, as it is
make flash_optimized   # Bonus    -- assemble your Bonus/flash_optimized.s, and print its size
```

Each of them (except `disassemble`) produces **`kernel7l.img`** in the main folder — that is the
file for the SD card. Only one program fits on the card at a time, so each build overwrites
`kernel7l.img`. That is on purpose.

Other targets: `make all` builds everything into `build/` without touching `kernel7l.img`;
`make sizes` lists how big each image is; `make clean` deletes the build output.

**On Windows** there is usually no `make`. Use the long way below — the commands are the same in
PowerShell.

---

## 4. Building — the long way

`make` only runs the commands below for you. Each section starts in the folder of that task.

### Task 1 — assemble `power_led.s`

```console
cd Task1
arm-none-eabi-as power_led.s -o kernel.elf
arm-none-eabi-objcopy kernel.elf -O binary kernel7l.img
```

The first command **assembles** the code: every line of assembly becomes one 4-byte machine
instruction, wrapped in an ELF file. The second strips the ELF wrapper and leaves the raw machine
code that the Pi's bootloader expects.

### Task 2 — investigate `kernel.elf`

Disassemble it and save the result as `kernel.s`:

```console
cd Task2-3
arm-none-eabi-objdump -d kernel.elf > kernel.s
```

Turn it into an image to run on the Pi. It is already an ELF file, so only the second step is
needed:

```console
arm-none-eabi-objcopy kernel.elf -O binary kernel7l.img
```

> ⚠️ **Never write `-o kernel.elf` inside `Task2-3/`.** That overwrites the very file you are
> investigating. If it happened, get it back with `git checkout -- Task2-3/kernel.elf`.

### Task 2.7 — compile your `led.c`

The same compiler flags as in Assignment 1:

```console
cd Task2-3
arm-none-eabi-gcc -g -nostartfiles -mfloat-abi=hard -O0 -DRPI4 \
    -mfpu=crypto-neon-fp-armv8 -march=armv8-a+crc -mcpu=cortex-a72 \
    led.c -o led.elf
arm-none-eabi-objcopy led.elf -O binary kernel7l.img
```

> You will see the warning `cannot find entry symbol _start`. That is expected, as in
> Assignment 1. Ignore it.

### Task 3 — reassemble your `reverse.s`

```console
cd Task2-3
arm-none-eabi-as reverse.s -o reverse.elf
arm-none-eabi-objcopy reverse.elf -O binary kernel7l.img
```

Why `kernel_clean.s` and not `kernel.s`? The disassembler's output carries addresses and raw
instruction bytes on every line, and branches point at numeric addresses — the assembler cannot
read that back in. `kernel_clean.s` is the same program, rewritten so that it can: just the
instructions, with labels such as `.L10` as branch targets.

### Task 4 — look at the raw bytes

```console
xxd kernel7l.img               # macOS, Linux, Codespaces
```

```powershell
Format-Hex kernel7l.img      # Windows PowerShell
```

In a Codespace you can also right-click the file → **Open With…** → **Hex Editor**.

### Bonus — make `flash.elf` smaller

Disassemble it first, exactly like `kernel.elf`:

```console
cd Bonus
arm-none-eabi-objdump -d flash.elf > flash.s
```

Write your optimized version as assembly in a new file **`flash_optimized.s`** (in the same
reassemblable style as `kernel_clean.s`), then:

```console
arm-none-eabi-as flash_optimized.s -o flash_optimized.elf
arm-none-eabi-objcopy flash_optimized.elf -O binary kernel7l.img
wc -c kernel7l.img                         # macOS, Linux: size in bytes
```

```powershell
(Get-Item kernel7l.img).Length            # Windows: size in bytes
```

The original `flash.elf` gives a 484-byte image. Leave `flash.elf` itself unchanged.

---

## 5. Working in a Codespace

The Codespace has the whole toolchain, `make` and `xxd`, so you can do all the disassembling,
assembling and byte-reading there.

It cannot do the rest: a Codespace has no SD card reader and no Raspberry Pi attached. For
anything that has to run on the Pi, build `kernel7l.img` on your own machine.

---

## 6. When something does not work

| Symptom | Usually means |
| --- | --- |
| `command not found: arm-none-eabi-as` | Toolchain not on PATH, or terminal opened before you set it. Open a new one; see section 1. |
| `command not found: make` | macOS: install Xcode command line tools (`xcode-select --install`). Windows: use the long way. |
| Assembler errors like `bad instruction` or `junk at end of line` on every line | You are assembling `objdump` output directly. Rewrite it in the style of `kernel_clean.s` (section 4, Task 3). |
| Assembler errors on line 1, on Windows | Windows PowerShell's `>` saves files as UTF-16, which the assembler cannot read. Save with `arm-none-eabi-objdump -d flash.elf \| Out-File -Encoding ascii flash.s` instead, or in VS Code: **Save with Encoding → UTF-8**. |
| `cannot find entry symbol _start` | Not an error. Expected. Ignore. |
| Pi does nothing at all | `kernel7l.img` missing or misnamed on the card, or the three `boot/` files are missing, or the card is not FAT32. |
| One or both LEDs never light | Check the wiring first: LED polarity (the long leg is +), the resistor, and the pins — physical pins **38** and **40** are BCM **20** and **21** ([pinout.xyz](https://pinout.xyz/)). |
| `git status` says `kernel.elf` or `flash.elf` is modified | You overwrote a given file. Restore it: `git checkout -- Task2-3/kernel.elf` (or `Bonus/flash.elf`). |
