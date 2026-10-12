#!/usr/bin/env python3
"""Completeness check for an Assignment 2 hand-in.

This does NOT grade anything and never looks at whether an answer is *correct* --
it only tells the student which parts of the hand-in are still missing, so nobody
loses points to an oversight. Run it locally with:

    python3 .github/scripts/check_submission.py
"""
from __future__ import annotations

import hashlib
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE_REPO = "2026-HS-ICS-Assignment2"
REPO_PREFIX = "ics-a2-group"
GRADERS = ("lukabekavac", "Karimkh31")

# Files we hand out and students must not change. If one of these differs, the
# student most likely overwrote it by accident (e.g. `as reverse.s -o kernel.elf`).
GIVEN_FILES = {
    "Task1/power_led.s": "3395f7aeedd9446303dd45c406de16c065cfa4400ef4dc2e2f46ff7e279ec916",
    "Task2-3/kernel.elf": "fb1aeeec695ea32f4cd4627e9c060540a423afa6b052a9b7a3033ca54c30aacd",
    "Task2-3/kernel_clean.s": "c6db3b3889f6dcb32e73fefc55808aa016a645e47bb4a699e5a2cd88d1a5a5c6",
    "Bonus/flash.elf": "7fd2ab96085f90e66e1ad7346eb7ccaf6a78fd06d9070df80475d15e7e4bab49",
}

# `TODO:` at the start of a line or at the start of a markdown table cell,
# ignoring any occurrence inside an inline `code span`.
CODE_SPAN = re.compile(r"`[^`]*`")
TODO = re.compile(r"(?:^|\|)\s*TODO:")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


class Report:
    def __init__(self) -> None:
        self.problems: list[tuple[str, str]] = []
        self.notes: list[str] = []

    def fail(self, what: str, detail: str) -> None:
        self.problems.append((what, detail))

    def note(self, msg: str) -> None:
        self.notes.append(msg)

    @property
    def ok(self) -> bool:
        return not self.problems


def find_todos(text: str) -> list[tuple[int, str]]:
    """Return (line number, enclosing heading) for every unfilled slot."""
    hits: list[tuple[int, str]] = []
    heading = "(top of file)"
    for n, raw in enumerate(text.splitlines(), start=1):
        m = HEADING.match(raw.strip())
        if m:
            heading = m.group(2).strip()
            continue
        if TODO.search(CODE_SPAN.sub("", raw)):
            hits.append((n, heading))
    return hits


def section_body(text: str, heading_substring: str) -> str:
    """Text between the heading containing `heading_substring` and the next heading."""
    lines = text.splitlines()
    start = None
    level = 0
    for i, raw in enumerate(lines):
        m = HEADING.match(raw.strip())
        if m and heading_substring.lower() in m.group(2).lower():
            start, level = i + 1, len(m.group(1))
            break
    if start is None:
        return ""
    out = []
    for raw in lines[start:]:
        m = HEADING.match(raw.strip())
        if m and len(m.group(1)) <= level:
            break
        out.append(raw)
    return "\n".join(out)


def table_value(section: str, field: str) -> str | None:
    """Value cell of a `| field | value |` row, or None if it is still blank."""
    m = re.search(r"^\|\s*" + re.escape(field) + r"[^|]*\|([^|]*)\|", section, re.M)
    if not m:
        return None
    value = m.group(1).strip()
    return None if not value or value.startswith("TODO:") else value


def read_report() -> str | None:
    path = ROOT / "REPORT.md"
    return path.read_text(encoding="utf-8") if path.exists() else None


def check_report(r: Report, text: str | None) -> str | None:
    if text is None:
        r.fail("REPORT.md", "File is missing -- it must not be renamed or deleted.")
        return None

    todos = find_todos(text)
    if todos:
        by_section: dict[str, list[int]] = {}
        for line, heading in todos:
            by_section.setdefault(heading, []).append(line)
        detail = "\n".join(
            f"  - **{heading}** — line(s) {', '.join(str(n) for n in lines)}"
            for heading, lines in by_section.items()
        )
        r.fail(
            "REPORT.md",
            f"{len(todos)} unanswered slot(s) still contain `TODO:`:\n{detail}",
        )

    team = section_body(text, "Team & process")
    group = table_value(team, "Group number")
    for field in ("Team member 1", "Team member 2"):
        if not table_value(team, field):
            r.fail(
                "REPORT.md",
                f"**{field}** is empty. You work in a group of two, so both names belong in "
                "the table at the top -- also if your partner did not touch the repository.",
            )
    if not group:
        r.fail("REPORT.md", "**Group number** is empty. Use the number from Canvas.")
    elif not re.fullmatch(r"\d+", group):
        r.fail(
            "REPORT.md",
            f"**Group number** is `{group}` -- please write digits only, e.g. `7`.",
        )
    return group


def check_repo_name(r: Report, group: str | None) -> None:
    """The repo name is how we match a hand-in to a group.

    This only ever warns: a freshly created repository is allowed to be red for the
    right reasons (unanswered questions), not for its name.
    """
    slug = os.environ.get("GITHUB_REPOSITORY", "")
    if not slug:
        return  # running locally; nothing to check against
    name = slug.split("/")[-1]
    if name == TEMPLATE_REPO:
        return  # this is the template itself, not a hand-in

    m = re.search(r"group0*(\d+)", name, re.I)
    if not m or not name.lower().startswith("ics-a2"):
        r.note(
            f"⚠️ **Please rename this repository.** It is called `{name}`, but it has to be "
            f"`{REPO_PREFIX}<your number>` — digits only, e.g. `{REPO_PREFIX}7` — so we can "
            "match it to your group. Do it under **Settings → General → Repository name**; "
            "links to the old name keep working, so it is safe to rename at any time."
        )
    elif group and m.group(1) != group.lstrip("0"):
        r.note(
            f"The repository is named `{name}` but `REPORT.md` says group **{group}**. "
            "One of the two is wrong -- please make them agree."
        )


def strip_c(src: str) -> str:
    """C source without comments and whitespace, so leftover comments don't count as work."""
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"//[^\n]*", "", src)
    return re.sub(r"\s+", "", src)


def strip_asm(src: str) -> str:
    """GNU ARM assembly without comments (`@`, `//`, `/* */`) and whitespace."""
    src = re.sub(r"/\*.*?\*/", "", src, flags=re.S)
    src = re.sub(r"(@|//)[^\n]*", "", src)
    return re.sub(r"\s+", "", src)


def check_given_files(r: Report) -> None:
    for name, digest in GIVEN_FILES.items():
        p = ROOT / name
        if not p.exists():
            r.note(
                f"`{name}` is missing. It is one of the files we gave you -- please copy it "
                "back from the assignment repository."
            )
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            r.note(
                f"`{name}` is not the file we gave you any more. That is usually an accident "
                "(e.g. `-o kernel.elf` in the wrong folder). Your own work belongs in "
                "`led.c`, `reverse.s` and `flash_optimized.s`; please restore the original "
                "from the assignment repository."
            )


def check_code(r: Report, report: str | None) -> None:
    led = ROOT / "Task2-3" / "led.c"
    if not led.exists():
        r.fail("Task2-3/led.c", "File is missing -- Task 2.7 needs it.")
    elif strip_c(led.read_text(encoding="utf-8")) == "intmain(void){}":
        r.fail(
            "Task2-3/led.c",
            "Still the empty starting file. Task 2.7 asks you to write the C code you think "
            "`kernel.elf` was compiled from.",
        )

    reverse, clean = ROOT / "Task2-3" / "reverse.s", ROOT / "Task2-3" / "kernel_clean.s"
    if not reverse.exists():
        r.fail("Task2-3/reverse.s", "File is missing -- Task 3 needs it.")
    elif clean.exists() and strip_asm(reverse.read_text(encoding="utf-8")) == strip_asm(
        clean.read_text(encoding="utf-8")
    ):
        r.fail(
            "Task2-3/reverse.s",
            "Still identical to `kernel_clean.s`. Task 3 asks you to show the LED patterns "
            "in reverse order.",
        )

    bonus = ROOT / "Bonus" / "flash_optimized.s"
    approach = section_body(report, "How did you approach it") if report else ""
    answered = approach.strip() and not find_todos(approach)
    declined = "not attempted" in approach.lower()
    if bonus.exists():
        if declined:
            r.note(
                "Section 5.1 says `not attempted`, but `Bonus/flash_optimized.s` exists. "
                "If you did attempt the bonus, explain your approach in 5.1."
            )
    elif answered and not declined:
        r.fail(
            "Bonus/flash_optimized.s",
            "Section 5.1 describes a bonus attempt, but the file is missing. Commit your "
            "optimized assembly as `Bonus/flash_optimized.s` -- or, if you did not do the "
            "bonus, write `not attempted` in 5.1.",
        )


def main() -> int:
    r = Report()
    report = read_report()
    group = check_report(r, report)
    check_repo_name(r, group)
    check_code(r, report)
    check_given_files(r)

    graders = " and ".join(f"`{g}`" for g in GRADERS)
    lines: list[str] = ["# Assignment 2 — submission check", ""]
    if r.ok:
        lines += [
            "✅ **Your hand-in looks complete.**", "",
            "This only checks that nothing is *missing* — it says nothing about whether "
            "your answers are right.", "",
            f"Before the deadline: make sure your partner, {graders} are collaborators "
            "here, and that **one** of you submits the repository URL on Canvas.",
        ]
    else:
        lines += [f"❌ **{len(r.problems)} thing(s) still to do.**", ""]
        for what, detail in r.problems:
            lines += [f"### `{what}`", "", detail, ""]

    if r.notes:
        # Leading "" matters: a `---` directly under text makes it a Markdown heading.
        lines += ["", "---", "", "### Notes", ""] + [f"- {n}" for n in r.notes]

    out = "\n".join(lines)
    print(out)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        Path(summary).write_text(out, encoding="utf-8")
    return 0 if r.ok else 1


if __name__ == "__main__":
    sys.exit(main())
