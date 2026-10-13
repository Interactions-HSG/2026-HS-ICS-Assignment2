# Assignment 2 -- Assembler Forensics
#
#   make power_led        assemble Task1/power_led.s            -> kernel7l.img     (Task 1)
#   make kernel           unpack the given Task2-3/kernel.elf   -> kernel7l.img     (Task 2)
#   make disassemble      disassemble Task2-3/kernel.elf        -> Task2-3/kernel.s (Task 2)
#   make led              compile your Task2-3/led.c            -> kernel7l.img     (Task 2.7)
#   make reverse          assemble your Task2-3/reverse.s       -> kernel7l.img     (Task 3)
#   make flash            unpack Bonus/flash.elf, print size    -> kernel7l.img     (Bonus)
#   make sizes            show the size of every image in build/
#   make all              build everything into build/ without touching kernel7l.img
#   make clean            remove build artifacts
#
# kernel7l.img is the file you copy onto the SD card. Only one program can be on the
# card at a time, so each target overwrites kernel7l.img -- that is intentional.
#
# No `make` on Windows? Use the commands in docs/TOOLCHAIN.md instead.

CROSS   ?= arm-none-eabi-

AS      := $(CROSS)as
CC      := $(CROSS)gcc
OBJCOPY := $(CROSS)objcopy
OBJDUMP := $(CROSS)objdump

# Same flags as in Assignment 1: the Raspberry Pi 400's BCM2711 (Cortex-A72) in 32-bit
# mode, with no C runtime startup files and no optimisation.
CFLAGS  := -g -nostartfiles -mfloat-abi=hard -O0 -DRPI4 \
           -mfpu=crypto-neon-fp-armv8 -march=armv8-a+crc -mcpu=cortex-a72

KERNEL  := kernel7l.img
BUILD   := build

# Size of the image of the flash.elf we hand out -- what the bonus is measured against.
FLASH_ORIGINAL := 484

PROGRAMS := power_led kernel led reverse flash

.PHONY: all sizes clean disassemble toolchain $(PROGRAMS)

# Build each program into build/ -- used by CI, leaves kernel7l.img alone.
all: $(addprefix $(BUILD)/,$(addsuffix .img,$(PROGRAMS)))

$(BUILD):
	@mkdir -p $(BUILD)

# Assembly -> ELF, with the GNU assembler.
$(BUILD)/power_led.elf:       Task1/power_led.s         | $(BUILD) ; $(AS) $< -o $@
$(BUILD)/reverse.elf:         Task2-3/reverse.s         | $(BUILD) ; $(AS) $< -o $@

# C -> ELF, with the compiler.
$(BUILD)/led.elf:             Task2-3/led.c             | $(BUILD) ; $(CC) $(CFLAGS) $< -o $@

# These two are already ELF files. (For the bonus, your own version replaces flash.elf.)
$(BUILD)/kernel.elf:          Task2-3/kernel.elf        | $(BUILD) ; cp $< $@
$(BUILD)/flash.elf:           Bonus/flash.elf           | $(BUILD) ; cp $< $@

# ELF -> raw image: strip the ELF wrapper, keep only the machine code the Pi boots.
$(BUILD)/%.img: $(BUILD)/%.elf
	$(OBJCOPY) $< -O binary $@

# `make reverse` etc.: build it, then put it where the SD card expects it.
$(filter-out flash,$(PROGRAMS)): %: $(BUILD)/%.img
	@cp $(BUILD)/$@.img $(KERNEL)
	@echo
	@echo "  Built $(KERNEL) from $@  ($$(wc -c < $(KERNEL) | tr -d ' ') bytes)"
	@echo "  Copy it to the root of your FAT32 SD card, eject, and boot the Pi."
	@echo

# Same as above, plus the number the bonus is graded on.
flash: $(BUILD)/flash.img
	@cp $(BUILD)/$@.img $(KERNEL)
	@new=$$(wc -c < $(KERNEL) | tr -d ' '); \
	 echo; \
	 echo "  Built $(KERNEL) from Bonus/flash.elf"; \
	 echo "  Size: $$new bytes  (the original flash.elf: $(FLASH_ORIGINAL) bytes, so $$(($(FLASH_ORIGINAL) - new)) bytes smaller)"; \
	 echo "  Copy it to the root of your FAT32 SD card, eject, and boot the Pi."; \
	 echo

disassemble: Task2-3/kernel.elf
	$(OBJDUMP) -d $< > Task2-3/kernel.s
	@echo "  Wrote Task2-3/kernel.s"

sizes: all
	@for f in $(BUILD)/*.img; do printf '  %-30s %5s bytes\n' "$$f" "$$(wc -c < $$f | tr -d ' ')"; done

toolchain:
	@command -v $(AS) >/dev/null || (echo "$(AS) not found -- see docs/TOOLCHAIN.md"; exit 1)
	@$(AS) --version | head -1
	@$(CC) --version | head -1
	@$(OBJCOPY) --version | head -1

clean:
	rm -rf $(BUILD) $(KERNEL)

.PRECIOUS: $(BUILD)/%.elf
