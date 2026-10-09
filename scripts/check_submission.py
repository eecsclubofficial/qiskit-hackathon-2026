#!/usr/bin/env python3
"""Self-check for a team's submission repository.

Usage:  python scripts/check_submission.py /path/to/team-repo

Checks the mechanical requirements only (files present, versions pinned, write-up page
count, obvious secrets). It cannot judge correctness or honesty: that is your job.
Exit code is 0 if all required checks pass, 1 otherwise.
"""
import os
import re
import subprocess
import sys

REQUIRED_README_WORDS = ["python", "pip install", "requirements"]
SECRET_PATTERNS = [
    re.compile(r"QISKIT_IBM_TOKEN\s*=\s*['\"]?[A-Za-z0-9_\-]{20,}"),
    re.compile(r"token\s*=\s*['\"][A-Za-z0-9_\-]{30,}['\"]", re.I),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
]
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules", ".ipynb_checkpoints"}


def pdf_pages(path):
    try:
        from pypdf import PdfReader
        return len(PdfReader(path).pages)
    except ImportError:
        pass
    try:
        out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        return int(m.group(1)) if m else None
    except FileNotFoundError:
        return None


def main():
    if len(sys.argv) != 2 or not os.path.isdir(sys.argv[1]):
        print(__doc__)
        return 2
    root = sys.argv[1]
    results = []  # (level, message) level in PASS/FAIL/WARN

    def ok(msg): results.append(("PASS", msg))
    def fail(msg): results.append(("FAIL", msg))
    def warn(msg): results.append(("WARN", msg))

    def exists(rel): return os.path.exists(os.path.join(root, rel))

    # README
    if exists("README.md"):
        text = open(os.path.join(root, "README.md"), encoding="utf-8", errors="ignore").read()
        ok("README.md present")
        low = text.lower()
        missing = [w for w in REQUIRED_README_WORDS if w not in low]
        if missing:
            warn("README should state the Python version and the install/run commands "
                 f"(missing mention of: {', '.join(missing)})")
        else:
            ok("README mentions Python, install and requirements")
        if "<project title>" in low or "<team name>" in low:
            fail("README still contains template placeholders (<project title>, <team name>, ...)")
    else:
        fail("README.md missing")

    # requirements
    req_path = os.path.join(root, "requirements.txt")
    if os.path.exists(req_path):
        lines = [l.strip() for l in open(req_path, encoding="utf-8", errors="ignore")
                 if l.strip() and not l.strip().startswith("#")]
        if not lines:
            fail("requirements.txt has no packages listed")
        else:
            unpinned = [l for l in lines if "==" not in l and not l.startswith(("-r", "-e", "git+", "http"))]
            if unpinned:
                fail(f"requirements.txt has unpinned packages (use ==): {', '.join(unpinned[:8])}")
            else:
                ok(f"requirements.txt pins all {len(lines)} packages")
    else:
        fail("requirements.txt missing")

    # write-up
    wp = os.path.join(root, "WRITEUP.pdf")
    if os.path.exists(wp):
        ok("WRITEUP.pdf present")
        n = pdf_pages(wp)
        if n is None:
            warn("Could not count WRITEUP.pdf pages (install pypdf or poppler); make sure it is 2-4 pages")
        elif 2 <= n <= 4:
            ok(f"WRITEUP.pdf is {n} pages")
        else:
            fail(f"WRITEUP.pdf is {n} pages; it must be 2-4 pages")
    else:
        fail("WRITEUP.pdf missing (2-4 pages: Problem, Method, Results, Honest limits)")

    # AI-use note
    ai = os.path.join(root, "AI_USE_NOTE.md")
    if os.path.exists(ai):
        t = open(ai, encoding="utf-8", errors="ignore").read()
        if "<A real, specific error" in t or "<Which AI tools" in t:
            fail("AI_USE_NOTE.md still contains template placeholder text")
        else:
            ok("AI_USE_NOTE.md present and filled in")
    else:
        warn("AI_USE_NOTE.md not found; the AI-use note must be in this file or inside WRITEUP.pdf")

    # figures
    fig_dir = os.path.join(root, "figures")
    figs = []
    if os.path.isdir(fig_dir):
        figs = [f for f in os.listdir(fig_dir) if f.lower().endswith((".png", ".jpg", ".jpeg", ".svg", ".pdf"))]
    if figs:
        ok(f"figures/ has {len(figs)} figure file(s)")
    else:
        fail("figures/ has no figure files (need at least one showing the main result)")

    # code
    code_files = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith((".py", ".ipynb")):
                code_files.append(os.path.join(dp, f))
    if code_files:
        ok(f"{len(code_files)} code file(s) found")
    else:
        fail("no .py or .ipynb files found")

    if exists("tests") and any(f for f in os.listdir(os.path.join(root, "tests")) if not f.startswith(".")):
        ok("tests/ present")
    else:
        warn("no tests found; checks against an exact or classical reference support the correctness score")

    # secrets
    leaked = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            if f.endswith((".py", ".ipynb", ".md", ".txt", ".env", ".json", ".yml", ".yaml", ".cfg", ".toml")):
                p = os.path.join(dp, f)
                try:
                    s = open(p, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                if any(pat.search(s) for pat in SECRET_PATTERNS):
                    leaked.append(os.path.relpath(p, root))
    if leaked:
        fail(f"possible API token/secret in: {', '.join(leaked)} (remove it and rotate the token)")
    else:
        ok("no obvious tokens found in files (also check your git history)")

    width = max(len(m) for _, m in results)
    for level, msg in results:
        print(f"[{level}] {msg}")
    fails = sum(1 for l, _ in results if l == "FAIL")
    warns = sum(1 for l, _ in results if l == "WARN")
    print(f"\n{fails} failure(s), {warns} warning(s).")
    print("Reminder: this only checks the mechanics. Also test a clean install in a fresh virtual environment.")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
