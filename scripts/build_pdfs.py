#!/usr/bin/env python3
"""Build the track PDFs and the guidelines PDF from content.py.

Usage (from the repo root):  python scripts/build_pdfs.py
Requires: reportlab (see requirements-organisers.txt)
"""
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak,
                                Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content as C  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACKS_DIR = os.path.join(ROOT, "tracks")
DOCS_DIR = os.path.join(ROOT, "docs")

ACCENT = colors.HexColor("#4F2D9E")
ACCENT_LIGHT = colors.HexColor("#EFE9FB")
GREY = colors.HexColor("#555555")

base = getSampleStyleSheet()
S = {
    "title": ParagraphStyle("title", parent=base["Title"], fontName="Helvetica-Bold",
                            fontSize=24, leading=28, textColor=ACCENT, alignment=TA_LEFT, spaceAfter=4),
    "subtitle": ParagraphStyle("subtitle", parent=base["Normal"], fontName="Helvetica",
                               fontSize=12, leading=16, textColor=GREY, spaceAfter=10),
    "h1": ParagraphStyle("h1", parent=base["Heading1"], fontName="Helvetica-Bold", fontSize=16,
                         leading=20, textColor=ACCENT, spaceBefore=14, spaceAfter=6),
    "h2": ParagraphStyle("h2", parent=base["Heading2"], fontName="Helvetica-Bold", fontSize=12.5,
                         leading=16, textColor=colors.black, spaceBefore=10, spaceAfter=4),
    "body": ParagraphStyle("body", parent=base["Normal"], fontName="Helvetica", fontSize=10,
                           leading=14.5, spaceAfter=6),
    "small": ParagraphStyle("small", parent=base["Normal"], fontName="Helvetica", fontSize=8.5,
                            leading=11, textColor=GREY),
    "cell": ParagraphStyle("cell", parent=base["Normal"], fontName="Helvetica", fontSize=9, leading=12),
    "cellb": ParagraphStyle("cellb", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12),
    "cellh": ParagraphStyle("cellh", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=9,
                            leading=12, textColor=colors.white),
    "callout": ParagraphStyle("callout", parent=base["Normal"], fontName="Helvetica", fontSize=10,
                              leading=14.5),
}


def P(text, style="body"):
    return Paragraph(text, S[style])


def bullets(items, style="body"):
    return ListFlowable(
        [ListItem(Paragraph(t, S[style]), leftIndent=14, bulletColor=ACCENT) for t in items],
        bulletType="bullet", start="•", leftIndent=14, bulletFontSize=9,
    )


def numbered(items, style="body"):
    return ListFlowable(
        [ListItem(Paragraph(t, S[style]), leftIndent=18) for t in items],
        bulletType="1", leftIndent=18, bulletFontName="Helvetica-Bold", bulletColor=ACCENT,
    )


def callout(text_html):
    t = Table([[Paragraph(text_html, S["callout"])]], colWidths=[170 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT_LIGHT),
        ("LINEBEFORE", (0, 0), (0, -1), 3, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def table(rows, col_widths, header=True):
    data = []
    for i, row in enumerate(rows):
        style = "cellh" if (header and i == 0) else "cell"
        data.append([Paragraph(str(c), S[style]) for c in row])
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    st = [
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), ACCENT))
        for r in range(2, len(rows), 2):
            st.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#F7F5FC")))
    t.setStyle(TableStyle(st))
    return t


def judging_table():
    rows = [["Criterion", "Points", "What judges look for"]]
    for name, pts, look in C.JUDGING:
        rows.append([f"<b>{name}</b>", str(pts), look])
    rows.append(["<b>Total</b>", f"<b>{sum(p for _, p, _ in C.JUDGING)}</b>",
                 "Bonus points are available on top for a real IBM hardware run (see Bonus)."])
    return table(rows, [48 * mm, 16 * mm, 106 * mm])


def make_doc(path, title, short_title):
    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, f"{C.EVENT['name']}  |  {short_title}")
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
        canvas.setStrokeColor(ACCENT)
        canvas.setLineWidth(1.2)
        canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
        canvas.restoreState()

    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                             topMargin=22 * mm, bottomMargin=20 * mm, title=title,
                             author=C.EVENT["host"])


def header_block(story, title, subtitle):
    story.append(P(title, "title"))
    story.append(P(subtitle, "subtitle"))
    story.append(P(f"{C.EVENT['name']} &middot; {C.EVENT['date']} &middot; {C.EVENT['host']}", "small"))
    story.append(Spacer(1, 8))


def common_deliverables(story):
    story.append(P("What every team submits", "h1"))
    story.append(P("Whichever problem you choose (or invent), your submission has the same five parts:"))
    story.append(bullets(C.DELIVERABLES))
    story.append(Spacer(1, 4))
    story.append(P("<b>Bonus.</b> " + C.BONUS))
    story.append(P("Full submission rules are in <i>docs/guidelines_and_submission_rules.pdf</i>."))
    story.append(P("How you are judged", "h1"))
    story.append(P("The same scoring applies to every problem and to original projects alike."))
    story.append(judging_table())
    story.append(Spacer(1, 6))
    story.append(callout("<b>On using AI.</b> " + C.AI_POLICY))


def build_track(track):
    path = os.path.join(TRACKS_DIR, track["slug"] + ".pdf")
    doc = make_doc(path, f"Track {track['n']}: {track['name']}", f"Track {track['n']}: {track['name']}")
    story = []
    header_block(story, f"Track {track['n']}: {track['name']}", track["tagline"])

    story.append(callout(
        "<b>Read this first.</b> " + C.READ_FIRST + "<br/><br/><b>What we reward.</b> " + C.WHAT_WE_REWARD
    ))
    story.append(P("How to read the problem statements", "h1"))
    story.append(P(C.HOW_LAID_OUT))
    story.append(P("<b>Simulators first, hardware as a bonus.</b> " + C.SIMULATORS_FIRST))

    probs = ", ".join(f"Problem {p['n']}" for p in track["problems"])
    story.append(P(f"This track contains: <b>{probs}</b>.", "body"))

    for prob in track["problems"]:
        story.append(PageBreak())
        story.append(P(f"Problem {prob['n']}: {prob['title']}", "h1"))
        story.append(P("Background", "h2"))
        story.append(P(prob["background"]))
        story.append(P("Problem", "h2"))
        story.append(P(prob["problem"]))
        story.append(P("Core tasks (the minimum for a complete submission)", "h2"))
        story.append(numbered(prob["core"]))
        story.append(P("Stretch goals (what makes it excellent)", "h2"))
        story.append(bullets(prob["stretch"]))
        story.append(P("Hints on tools", "h2"))
        story.append(P(prob["hints"]))

    # Relevant combined-project ideas
    ideas = [g for g in C.GO_BEYOND if track["n"] in g[2]]
    story.append(PageBreak())
    story.append(P("Go beyond: combine tracks or invent your own", "h1"))
    story.append(P("The most impressive entries will not stop at one box. None of these is required, "
                   "and you are free to propose something entirely different."))
    if ideas:
        story.append(P(f"Ideas that involve Track {track['n']}", "h2"))
        rows = [["Idea", "Tracks combined", "What makes it interesting"]]
        for idea, combo, _, why in ideas:
            rows.append([f"<b>{idea}</b>", combo, why])
        story.append(table(rows, [45 * mm, 45 * mm, 80 * mm]))
    story.append(Spacer(1, 6))
    story.append(P("<b>Open invitation.</b> " + C.OPEN_INVITATION))
    story.append(P("<b>How to scope a combined project.</b> " + C.HOW_TO_SCOPE))

    story.append(PageBreak())
    common_deliverables(story)

    doc.build(story, onFirstPage=lambda c, d: _deco(c, d, track), onLaterPages=lambda c, d: _deco(c, d, track))
    return path


def _deco(canvas, doc, track):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(20 * mm, 12 * mm, f"{C.EVENT['name']}  |  Track {track['n']}: {track['name']}")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
    canvas.restoreState()


def _deco_guidelines(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GREY)
    canvas.drawString(20 * mm, 12 * mm, f"{C.EVENT['name']}  |  Guidelines and Submission Rules")
    canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, f"Page {doc.page}")
    canvas.setStrokeColor(ACCENT)
    canvas.setLineWidth(1.2)
    canvas.line(20 * mm, A4[1] - 14 * mm, A4[0] - 20 * mm, A4[1] - 14 * mm)
    canvas.restoreState()


def build_guidelines():
    path = os.path.join(DOCS_DIR, "guidelines_and_submission_rules.pdf")
    doc = make_doc(path, "Guidelines and Submission Rules", "Guidelines and Submission Rules")
    ph = C.PLACEHOLDERS
    story = []
    header_block(story, "Guidelines and Submission Rules",
                 "Everything you need to know to take part, build, submit and be judged")

    story.append(callout("<b>The one-line version.</b> Build something that works, explain every line of it, "
                         "compare it honestly against a classical alternative, and put it all in a GitHub "
                         "repository that runs from a clean start."))

    story.append(P("1. Event at a glance", "h1"))
    story.append(table([
        ["Item", "Details"],
        ["Event", f"{C.EVENT['name']}, hosted by {C.EVENT['host']}"],
        ["Kick-off", f"{C.EVENT['date']} ({C.EVENT['venue']})"],
        ["Duration", f"{C.EVENT['duration']} to build"],
        ["Submission deadline", ph["deadline"]],
        ["Team size", ph["team_size"]],
        ["Where to submit", ph["submit_channel"]],
        ["Questions", ph["contact"]],
        ["Tools", "Laptop and AI assistants. Everything can be done on a simulator (Qiskit Aer or statevector tools)."],
    ], [40 * mm, 130 * mm]))

    story.append(P("2. Choosing a project", "h1"))
    story.append(P(C.READ_FIRST))
    story.append(bullets([
        "<b>Six tracks, ten suggested problems:</b> Quantum chemistry (Problems 1-2), Quantum machine learning (3-4), "
        "QAOA and optimisation (5-6), Quantum error correction (7-8), Quantum key distribution (9), "
        "Post-quantum cryptography (10).",
        "<b>Core tasks are the minimum, not the ceiling.</b> Stretch goals, combined tracks and original ideas "
        "score on ambition and originality.",
        "<b>Own idea?</b> " + C.OPEN_INVITATION,
        "<b>Combining tracks?</b> " + C.HOW_TO_SCOPE,
    ]))

    story.append(P("3. What you must submit", "h1"))
    story.append(P("Every team submits the following. Missing items cost points, because each one maps to a "
                   "judging criterion."))
    story.append(table([
        ["#", "Deliverable", "Requirement"],
        ["1", "<b>GitHub repository</b>",
         "All code in one public repository (or private with the organisers added as collaborators). Runs from a clean "
         "start, with the versions of all packages listed."],
        ["2", "<b>Write-up PDF</b>",
         "One PDF of two to four pages, stored in the repo root as <font face='Courier'>WRITEUP.pdf</font>. Sections: "
         "Problem, Method, Results, and an honest Limits section."],
        ["3", "<b>Main-result figure</b>",
         "At least one figure that shows the main result, included in the write-up and saved in "
         "<font face='Courier'>figures/</font>."],
        ["4", "<b>AI-use note</b>",
         "Short note: which tools you used, one thing the AI got wrong, and how you caught it. Included in the "
         "write-up and/or as <font face='Courier'>AI_USE_NOTE.md</font>."],
        ["5", "<b>Demo</b>",
         "Five-minute demo followed by questions. Every team member must be able to take questions."],
    ], [8 * mm, 40 * mm, 122 * mm]))
    story.append(Spacer(1, 4))
    story.append(P("<b>Bonus.</b> " + C.BONUS + " Include the backend name, the date of the run, the job ID, "
                   "and a side-by-side comparison with your simulator result."))

    story.append(P("4. Repository rules", "h1"))
    story.append(P("Your repository is the main artefact judges will run and read. Use the structure in "
                   "<font face='Courier'>submission-template/</font> as a starting point."))
    story.append(P("Required contents", "h2"))
    story.append(table([
        ["Path", "Purpose"],
        ["<font face='Courier'>README.md</font>",
         "Team name and members, chosen problem or project title, one-paragraph summary, exact commands to reproduce "
         "your main result, and expected runtime."],
        ["<font face='Courier'>requirements.txt</font>",
         "Every package with its version pinned (<font face='Courier'>package==x.y.z</font>), plus the Python version."],
        ["<font face='Courier'>WRITEUP.pdf</font>", "Your two-to-four page write-up."],
        ["<font face='Courier'>AI_USE_NOTE.md</font>", "The AI-use note (may also appear inside the write-up)."],
        ["<font face='Courier'>src/</font> or notebooks", "Your code. Readable, commented where it is not obvious."],
        ["<font face='Courier'>figures/</font>", "All figures used in the write-up, including the main-result figure."],
        ["<font face='Courier'>tests/</font>", "Tests or checks against an exact or classical reference (recommended; supports the "
                                             "correctness criterion)."],
    ], [48 * mm, 122 * mm]))
    story.append(P("Reproducibility: a clean start", "h2"))
    story.append(numbered([
        "Create a fresh virtual environment (for example <font face='Courier'>python -m venv .venv</font>).",
        "Run <font face='Courier'>pip install -r requirements.txt</font> and nothing else.",
        "Run the commands in your README. The main result and main figure must be produced without manual edits.",
        "Fix random seeds so results can be reproduced, and state in the README which results are statistical and "
        "how many runs they average over.",
        "If any step needs an IBM Quantum account or API token, say so, and <b>never commit your token</b>. Use an "
        "environment variable and provide a simulator-only path that works without it.",
        "Before submitting, test steps 1-3 on a machine or folder that is not your development setup.",
    ]))
    story.append(P("Listing package versions", "h2"))
    story.append(P("Run <font face='Courier'>pip freeze &gt; requirements.txt</font> inside your project environment "
                   "and trim it to the packages you actually use, or write them by hand. Qiskit and its add-on "
                   "packages change quickly between releases, so exact versions matter. Also record your Python "
                   "version in the README."))

    story.append(P("5. The write-up (2 to 4 pages)", "h1"))
    story.append(table([
        ["Section", "What to include"],
        ["Problem", "The problem you chose or invented, why it matters, and what a successful result looks like."],
        ["Method", "What you built and how: circuits, encodings, parameters, optimisers, noise models. Enough detail "
                   "that a reader could rebuild it."],
        ["Results", "Your main result with the key figure, numbers with sensible error bars, and the comparison against "
                    "an exact or classical reference."],
        ["Honest limits", "What does not work, what you did not test, assumptions, which parts are a simulation shortcut, "
                          "and where a classical method does as well or better. No unsupported claims of quantum advantage."],
        ["AI-use note", "Tools used, one thing the AI got wrong, how you caught it."],
    ], [32 * mm, 138 * mm]))
    story.append(Spacer(1, 4))
    story.append(P("Keep to four pages. Figures and tables count toward the page limit. Put extra material in the "
                   "repository and link to it."))

    story.append(P("6. Using AI", "h1"))
    story.append(callout(C.AI_POLICY))
    story.append(Spacer(1, 4))
    story.append(bullets([
        "AI use is welcome at every step: ideas, code, debugging, writing.",
        "The AI-use note must be specific. <b>\"The AI sometimes makes mistakes\" is not acceptable.</b> Name one real "
        "error (a wrong gate, a wrong formula, a hallucinated function, a misleading explanation) and describe the "
        "check that caught it, such as a test, a comparison with exact diagonalisation, or a known limiting case.",
        "In the live questions, any team member may be asked to explain any circuit, formula or plot. If you cannot "
        "explain or verify code, it will cost you marks under <i>Understanding and insight</i> and <i>Correctness and "
        "verification</i>.",
        "Do not present AI-generated text or results as verified when you have not verified them.",
    ]))

    story.append(P("7. Honesty rules", "h1"))
    story.append(bullets([
        "<b>Compare against a classical baseline.</b> Every result needs a fair classical comparison with similar "
        "resources (for example a similar number of parameters).",
        "<b>Do not claim a quantum speedup or advantage</b> unless your measurements actually show one under a fair comparison. "
        "Results that say \"no advantage, and here is why\" are valued.",
        "<b>Say what is simulated.</b> Distinguish a physical circuit simulation from a statistical shortcut, and a "
        "noiseless simulator from a noise model from real hardware.",
        "<b>Report negative and weak results.</b> A clear failure analysis scores better than hidden weak results.",
        "<b>Cryptography code is for learning only.</b> Toy schemes (Track 6, and QKD post-processing) must never be "
        "used to protect real data, and you must say so in your README.",
    ]))

    story.append(P("8. The demo and live questions", "h1"))
    story.append(bullets([
        "<b>Five minutes</b> for the demo, then questions. Keep to time.",
        "Tell a clear story: the problem, what you built, the main result, and what it does not show.",
        "Show something running, or a recorded run of the main result as a fallback.",
        "<b>Every team member must be present and able to take questions.</b>",
        "Have the repository open and runnable on the day. Judges may ask you to run or step through a part of the code.",
    ]))

    story.append(P("9. How you are judged", "h1"))
    story.append(P("The scoring below applies to every problem and to original projects alike."))
    story.append(judging_table())
    story.append(Spacer(1, 6))
    story.append(P("<b>Bonus:</b> " + C.BONUS))

    story.append(P("10. Integrity and conduct", "h1"))
    story.append(bullets([
        "Work must be produced by your team during the hackathon week. Cite any code, data, papers or tutorials you "
        "build on (for example the IBM SQD tutorials), and make clear what you added.",
        "Using open-source libraries (Qiskit, PySCF, ldpc, stim and so on) is expected. Importing a library call that "
        "does the whole task is allowed, but where a problem says to build something yourself, building it yourself "
        "is what earns the marks.",
        "Do not copy another team's work. Do not share API tokens, credentials or personal data in your repository.",
        "Be respectful to participants, volunteers and judges. Organisers may disqualify submissions that break these rules.",
    ]))

    story.append(P("11. Final checklist", "h1"))
    story.append(P("Tick every box before you submit."))
    boxes = [
        "Repository runs from a clean start; <font face='Courier'>requirements.txt</font> has pinned versions and README states the Python version",
        "README gives exact commands and expected runtime for the main result",
        "<font face='Courier'>WRITEUP.pdf</font> is 2-4 pages with Problem, Method, Results and Honest limits",
        "At least one figure shows the main result",
        "Results are checked against an exact or classical reference, and a classical baseline is included",
        "AI-use note names the tools, one specific AI error, and how you caught it",
        "No API tokens or secrets in the repository or git history",
        "Hardware run (optional bonus) is compared clearly against the simulator",
        "Every team member can explain every circuit, formula and plot, and can take questions in the demo",
        f"Submitted via {ph['submit_channel']} before {ph['deadline']}",
    ]
    story.append(table([["Done", "Item"]] + [["[  ]", b] for b in boxes], [14 * mm, 156 * mm]))

    story.append(P("12. Getting help", "h1"))
    story.append(P(f"Check with the organisers early in the week if you are unsure about scope, a custom idea, or "
                   f"any rule above: {ph['contact']}."))

    doc.build(story, onFirstPage=_deco_guidelines, onLaterPages=_deco_guidelines)
    return path


def main():
    os.makedirs(TRACKS_DIR, exist_ok=True)
    os.makedirs(DOCS_DIR, exist_ok=True)
    for t in C.TRACKS:
        print("built", build_track(t))
    print("built", build_guidelines())


if __name__ == "__main__":
    main()
