# Assignment 2: Assembler Forensics

**Einführung in Computersysteme — HS 2026 · 10 points + bonus · Deadline: 22 November 2026, 23:59 CET**

You will read, reverse-engineer and write **assembly code** for the Raspberry Pi, and translate
instructions into raw machine code by hand. 📄 The questions and all the detail are in
**[`docs/assignment2.pdf`](docs/assignment2.pdf)**. This page is only about *how to work and
hand in*.

**You need:** a Raspberry Pi 400 PC-Kit, two 330 Ω resistors, two LEDs, a breadboard, and some
jumper wires.

**You work in your assigned group of two.** You share **one** repository: one of you creates
it, the other joins as a collaborator. Only one of you hands in.

**Same procedure as in Assignment 1** — but with a **new** repository. Do not reuse your
Assignment 1 repository. If you have done this before, skim the steps; the only things that
change are the template link and the name `ics-a2-group<N>`.

*Original repository: <https://github.com/Interactions-HSG/2026-HS-ICS-Assignment2>*

---

## Step 1 · One of you makes the copy

> **Decide who does this — only one of you.** If your partner already created the repository,
> skip to Step 3 and ask them to add you.

On the [assignment repository](https://github.com/Interactions-HSG/2026-HS-ICS-Assignment2),
click the green **`Use this template`** → **`Create a new repository`**.

Then:

| Setting | What to choose |
| --- | --- |
| Repository name | `ics-a2-group<your number>`, e.g. **`ics-a2-group7`** |
| Visibility | **Private** ← important |

Your **group number** is the one from the group assignment on Canvas. Use digits only, no
spaces: `ics-a2-group7`, not `ics-a2-Group 7` or `ics-a2-gruppe7`. We match repositories to
groups by that name, so getting it right saves everyone time.

Click **Create repository**. Your group now has its repository at
`github.com/your-username/ics-a2-group7`.

> **Why not "Fork"?**
> You may have seen a **Fork** button on GitHub. Forking also copies a project, but a fork of
> a public project is **always public** — everyone in the course could read your answers.
> **Use this template** gives you a private copy instead. So: template, not fork.

## Step 2 · Add your partner and us

The repository is private, so right now *nobody* can see it — not your partner, not us. Whoever
created it goes to:

**Settings** → **Collaborators** → **Add people**, and adds **three** people:

```
<your partner's GitHub username>
lukabekavac
Karimkh31
```

Your partner then gets an email invitation and has to **accept** it before they can push.

> ⚠️ **Forget this and we cannot open your repository, so we cannot grade you.** Do it now, not
> on the deadline.

## Step 3 · Open your repository

You have two options. **Codespaces is the easy one** — start there.

### Option A — Codespaces (recommended)

In **your** repository: **`Code ▾`** → **`Codespaces`** → **`Create codespace on main`**.

> **What is a Codespace?** A complete Linux computer running in your browser: a code editor, a
> terminal, and all the tools for this assignment already installed. Nothing to install on your
> laptop. Your files live in your repository, so you can close the tab and come back later.
> GitHub gives every account a free monthly allowance, far more than this assignment needs.

The first start takes 2–3 minutes while the toolchain downloads. After that it opens in seconds.

💡 When you are done for the day, close the Codespace (**`Code ▾` → `Codespaces` → `...` →
`Stop codespace`**) so it does not use up your free hours.

### Option B — On your own computer

In a terminal:

```console
$ git clone https://github.com/your-username/ics-a2-group7.git
$ cd ics-a2-group7
```

`clone` means "download this repository onto my computer, and remember where it came from".
Use the URL of **your group's** repository, not the one you are reading now.

## Step 4 · Answer the questions

Open **[`REPORT.md`](REPORT.md)**. Together with your code, that file *is* your hand-in — there
is no zip file and nothing to upload.

Every place that needs an answer from you holds a line that starts with `TODO:`. Replace that
whole line with your answer. That's the entire trick.

Your code goes into three files: `Task2-3/led.c` (Task 2.7), `Task2-3/reverse.s` (Task 3) and,
for the bonus, a new file `Bonus/flash_optimized.s`.

## Step 5 · Save your work (this is what Git is for)

Editing a file is not enough — you have to **commit** it (take a snapshot) and **push** it
(upload that snapshot to GitHub). Until you push, we see nothing.

**In Codespaces or VS Code**, use the **Source Control** panel on the left (the branching icon):
type a short message, click **Commit**, then click **Sync Changes**. That's it.

**In a terminal**, the same thing in three commands:

```console
$ git add .                        # which changes go into the snapshot -- "." means all of them
$ git commit -m "Answered task 2"  # take the snapshot, with a short note about what you did
$ git push                         # upload it to GitHub
```

Do this often — after every task, not once at the end. It costs 10 seconds and it means a
crashed browser cannot eat your evening.

> **Working with your partner:** you share one repository, so run `git pull` (or click
> **Sync Changes**) *before* you start working, to get their latest changes. If you both edit
> the same lines at the same time, Git will ask you to sort out the conflict — easiest to avoid
> by agreeing who does which task.

**Check it worked:** open your repository on github.com and look at `REPORT.md`. If your
answers are there, you are safe.

### You get automatic feedback

Every time you push, a check runs and tells you what is still missing: unanswered questions,
code you have not touched yet, code that does not assemble or compile. Click the **Actions** tab
of your repository to see it — a green ✓ means nothing is missing, a red ✗ tells you exactly
what to fix. For the bonus, it also tells you how many bytes your image has.

It checks **completeness, not correctness**. Green does not mean your answers are right.

## Step 6 · Hand in

1. No `TODO:` lines left in `REPORT.md` — including your **group number** and **both names**
   at the top
2. Everything **pushed** (Step 5)
3. Your partner, `lukabekavac` and `Karimkh31` added as collaborators (Step 2)
4. **One of you** — not both — submits **only the repository URL** on Canvas:
   `https://github.com/your-username/ics-a2-group7`

We grade whatever is on your `main` branch at the deadline. Both of you get the same mark.

---

## One thing Codespaces cannot do

A Codespace lives in a data centre. It cannot reach your SD card reader and it cannot power
your Raspberry Pi. Disassembling, assembling and reading bytes all work fine in the Codespace —
but for everything you run on the Pi (Tasks 1, 2.1, 3 and the bonus), build `kernel7l.img` on
**your own laptop**, with the toolchain you installed in Assignment 1.

👉 **[`docs/TOOLCHAIN.md`](docs/TOOLCHAIN.md)** has every command, task by task, and what to do
when something does not work.

## What's in this repository

| File | What it is |
| --- | --- |
| **`REPORT.md`** | **Your hand-in.** Answer the questions here. |
| `Task1/power_led.s` | **Task 1.** Given to you. Turns off the power LED. |
| `Task2-3/kernel.elf` | **Task 2.** The program you investigate. Don't change it. |
| `Task2-3/kernel_clean.s` | **Task 2.** The same program as assembly you can reassemble. Don't change it. |
| `Task2-3/led.c` | **Task 2.7.** Empty — your C reconstruction of `kernel.elf` goes here. |
| `Task2-3/reverse.s` | **Task 3.** Starts as a copy of `kernel_clean.s` — make it run in reverse. |
| `Bonus/flash.elf` | **Bonus.** The program to shrink. Don't change it — your version goes in a new `Bonus/flash_optimized.s`. |
| `boot/` | Firmware for your SD card — the same as in Assignment 1. |
| `docs/` | The assignment sheet, the command guide, the Arm Architecture Reference Manual, and the BCM2711 manual. |
| `Makefile` | Build shortcuts: `make reverse` and friends. |

## Stuck?

- The **[Arm Architecture Reference Manual](docs/DDI0487Fc_armv8_arm.pdf)** (version F.c — the
  section numbers on the sheet refer to this version). It has over 8000 pages: don't read it,
  *search* it. The sheet tells you which sections matter.
- The [AArch32 Base Instructions](https://developer.arm.com/documentation/ddi0597/2021-12/Base-Instructions?lang=en)
  reference — one page per instruction, easier to browse than the manual.
- [armconverter.com](https://armconverter.com/) — translates between ARM assembly and hex, so
  you can check an encoding you worked out by hand. (Do the work by hand first — that is what
  Task 4 is about.)
- [pinout.xyz](https://pinout.xyz/) — which physical pin is which GPIO number.
- The **[BCM2711 ARM Peripherals manual](docs/bcm2711-peripherals.pdf)** from Assignment 1 —
  the GPIO registers on pages **65–70** (`GPFSEL`, `GPSET`, `GPCLR`) are exactly what
  `kernel.elf` writes to.
- **For Task 2, use an AI assistant** — the sheet asks you to. Ask it to *explain*, and check
  what it says against the manual: it is often confidently wrong about addresses and bit fields.
  Write down what you used in section 0.4 of the report.
- Come to the exercise session, or ask in your repository's **Issues** tab and mention
  `@lukabekavac` or `@Karimkh31`.

## Contact

- Luka Bekavac — <luka.bekavac@unisg.ch> · GitHub `lukabekavac`
- Karim Khamaisi — <karim.khamaisi@unisg.ch> · GitHub `Karimkh31`
- Simon Mayer — <simon.mayer@unisg.ch>

## License

MIT — see [`LICENSE`](LICENSE).
