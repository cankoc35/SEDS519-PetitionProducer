"""PDF export helpers for formal petition output."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def _latex_escape(text: str) -> str:
    """Escape LaTeX special characters in user-provided text."""
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    escaped = []
    for char in text:
        escaped.append(replacements.get(char, char))
    return "".join(escaped)


def build_petition_pdf_tex(petition: object) -> str:
    """Return a minimal formal A4 LaTeX document for a petition."""
    title = _latex_escape(str(getattr(petition, "title", "")))
    receiver = _latex_escape(str(getattr(petition, "receiver", "-")))
    petitioner = _latex_escape(str(getattr(petition, "petitioner", "-")))
    body = _latex_escape(str(getattr(petition, "body", ""))).replace("\n", "\n\n")
    attachments = getattr(petition, "attachments", [])

    if attachments:
        attachment_section = (
            "\\textbf{Attachments}\n"
            "\\begin{itemize}[leftmargin=1.5em]\n"
            + "\n".join(
                f"\\item {_latex_escape(Path(str(attachment)).name)}"
                for attachment in attachments
            )
            + "\n\\end{itemize}"
        )
    else:
        attachment_section = ""

    return rf"""\documentclass[12pt,a4paper]{{article}}
\usepackage[margin=20mm]{{geometry}}
\usepackage[T1]{{fontenc}}
\usepackage[utf8]{{inputenc}}
\usepackage{{mathptmx}}
\usepackage{{enumitem}}
\pagestyle{{empty}}
\setlength{{\parindent}}{{0pt}}
\setlength{{\parskip}}{{1em}}

\begin{{document}}

\textbf{{{title}}}

Receiver: {receiver}

Petitioner: {petitioner}

{body}

{attachment_section}

\end{{document}}
"""


def export_petition_pdf(petition: object, target_path: Path) -> Path:
    """Render the petition as a formal A4 PDF and save it to the target path."""
    pdflatex = shutil.which("pdflatex")
    if pdflatex is None:
        raise RuntimeError("pdflatex is not installed, so PDF export is unavailable.")

    target_path = target_path.with_suffix(".pdf")

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        tex_path = tmp_path / "petition.tex"
        pdf_path = tmp_path / "petition.pdf"
        tex_path.write_text(build_petition_pdf_tex(petition), encoding="utf-8")

        subprocess.run(
            [pdflatex, "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf_path, target_path)

    return target_path
