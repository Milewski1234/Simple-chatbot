import os
from typing import Dict, List

from loaders.pdf_loader import load_pdf
from loaders.markdown_loader import load_markdown
from loaders.text_loader import load_text
from services.hr_service import HRService


# ============================================================
# Document Ingestion
# ============================================================

def load_document(path: str) -> Dict:
    """
    Load a document and normalize it into a list of semantic sections.
    All document types must expose the same contract:
    {
        "source": str,
        "sections": List[str]
    }
    """

    if path.endswith(".pdf"):
        sections = load_pdf(path)

    elif path.endswith(".md"):
        text = load_markdown(path)
        sections = []
        buffer = []

        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Markdown heading
            if line.startswith("#"):
                if buffer:
                    sections.append(" ".join(buffer))
                    buffer = []
                buffer.append(line.lstrip("#").strip())
            else:
                buffer.append(line)

        if buffer:
            sections.append(" ".join(buffer))

    elif path.endswith(".txt"):
        text = load_text(path)
        sections = [s.strip() for s in text.split("\n\n") if s.strip()]

    else:
        raise ValueError("Unsupported document format")

    return {
        "source": os.path.basename(path),
        "sections": sections
    }


def load_all_documents(folder: str = "documents") -> List[Dict]:
    documents = []

    for filename in os.listdir(folder):
        if not filename.lower().endswith((".pdf", ".md", ".txt")):
            continue

        path = os.path.join(folder, filename)

        try:
            documents.append(load_document(path))
        except Exception as e:
            print(f"⚠️ Skipping {filename}: {e}")

    return documents


# ============================================================
# Static Retrieval (Keyword + Intent Aware)
# ============================================================

STOPWORDS = {
    "the", "is", "are", "of", "to", "a", "an", "what", "how",
    "do", "does", "i", "my", "can", "when", "time"
}

# Phrase normalization to handle paraphrases
NORMALIZATION_MAP = {
    "workday start": "working hours",
    "workday end": "working hours",
    "workday begin": "working hours",
    "start time": "working hours",
    "end time": "working hours",
}

# Lightweight intent hints to avoid semantic collisions
INTENT_HINTS = {
    "conduct": {"behave", "behavior", "conduct", "professional", "respectful"},
    "vacation": {"vacation", "leave", "days"},
    "work": {"work", "working", "hours", "workday"},
    "remote": {"remote"},
}


def normalize_question(question: str) -> str:
    q = question.lower()
    for k, v in NORMALIZATION_MAP.items():
        q = q.replace(k, v)
    return q


def search_documents(question: str, documents: List[Dict]) -> str:
    """
    Deterministic, explainable document retrieval.
    Uses keyword overlap + intent-aware boosting.
    """

    question = normalize_question(question)

    tokens = [
        t for t in question.split()
        if t not in STOPWORDS
    ]

    if not tokens:
        return "I couldn't find relevant information in the documents."

    best_match = None
    best_score = 0

    for doc in documents:
        for section in doc["sections"]:
            section_lower = section.lower()

            # Base keyword score
            score = sum(1 for t in tokens if t in section_lower)

            # Intent-aware boost
            for intent, intent_tokens in INTENT_HINTS.items():
                if any(t in tokens for t in intent_tokens) and intent in section_lower:
                    score += 2

            if score > best_score:
                best_score = score
                best_match = section

    # Confidence gate
    if best_score < 1:
        return "I couldn't find relevant information in the documents."

    return best_match


# ============================================================
# Dynamic Routing (Authoritative External Data)
# ============================================================

DYNAMIC_PATTERNS = [
    ("vacation", "left"),
    ("vacation", "remaining"),
    ("vacation", "still"),
    ("vacation", "balance"),
]


def is_dynamic_query(question: str) -> bool:
    q = question.lower()
    return any(a in q and b in q for a, b in DYNAMIC_PATTERNS)


def chatbot_answer(question: str, documents: List[Dict]) -> str:
    """
    Central orchestration logic.
    Decides source of truth (static docs vs dynamic services).
    """

    if is_dynamic_query(question):
        hr = HRService()
        days = hr.get_remaining_vacation_days(user_id="demo-user")
        return f"You have {days} vacation days remaining."

    return search_documents(question, documents)
