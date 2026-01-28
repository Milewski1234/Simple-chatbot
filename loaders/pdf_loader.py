import pdfplumber
from typing import List


def _split_into_sections(text: str) -> List[str]:
    sections = []
    buffer = []

    HEADING_HINTS = {
        "vacation policy",
        "working hours",
        "code of conduct",
        "remote work policy",
        "security policy",
    }

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        lower = line.lower()

        is_heading = (
            lower in HEADING_HINTS
            or lower.endswith("policy")
            or line.isupper()
        )

        if is_heading and buffer:
            sections.append(" ".join(buffer))
            buffer = []

        buffer.append(line)

    if buffer:
        sections.append(" ".join(buffer))

    return sections


def load_pdf(path: str) -> List[str]:
    try:
        pages = []

        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)

        if not pages:
            raise RuntimeError("PDF contains no extractable text")

        full_text = "\n".join(pages)
        sections = _split_into_sections(full_text)

        return sections if sections else [full_text.strip()]

    except Exception as e:
        raise RuntimeError(f"Failed to load PDF '{path}': {e}")
