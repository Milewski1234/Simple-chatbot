# Simple Multi-Source Chatbot (CLI)

## Overview

This project implements a lightweight, CLI-based chatbot that can:

- Answer questions using **static, multi-format documents** (PDF, Markdown, TXT)
- Retrieve **dynamic, user-specific information** from an external service (mocked)
- Decide which **source of truth** to use based on the user’s question

The primary goal of this project is **architectural clarity**, not production-scale AI.
It focuses on clean separation of concerns, explainable behavior, and safe defaults.

No Large Language Model (LLM) and no database are used by design.

---

## Key Concepts

- **Static knowledge**: Company policies and documentation stored in files  
- **Dynamic knowledge**: User-specific, frequently changing data retrieved on demand  
- **Source-of-truth routing**: The system decides whether to consult documents or an external service  

---

## Architecture Summary

The system is structured into clear, independent layers:

- **CLI Layer**  
  Handles user input and output only.

- **Query Orchestrator**  
  Interprets the question and routes it to the correct data source.

- **Document Ingestion Layer**  
  Loads and normalizes PDF, Markdown, and TXT files into semantic sections.

- **Static Retriever**  
  Searches document sections using deterministic, explainable logic.

- **Dynamic Service Client**  
  Fetches authoritative, user-specific data from an external system (mocked HR service).

The architecture explicitly separates **static knowledge** from **dynamic state**.

---

## Assumptions

- “Multi-modal” refers to **multiple document formats**, not multimodal AI (images/audio).
- Documents contain **static, shared knowledge** (policies, rules).
- Dynamic data (e.g., vacation balance) must come from an **authoritative external system**.
- The system owns **no mutable state**.
- Determinism and explainability are preferred over probabilistic AI behavior.

---

## Prerequisites

Before running the project, make sure you have:

- **Python 3.9 or newer**
- **pip** (Python package manager)
- Internet access (to install dependencies)

You can verify your Python version with:

```bash
python --version
```

## Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/Milewski1234/Simple-chatbot.git
cd simple-chatbot
```

### 2. Create a virtual environment (recommended)

Using a virtual environment avoids dependency conflicts.

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You should now see (venv) in your terminal prompt.

### 3. Install project dependencies

All required dependencies are listed in requirements.txt.

```bash
pip install -r requirements.txt
```

This installs:
* pdfplumber (for PDF text extraction)

No other dependencies are required.

## Project Structure

```bash
simple-chatbot/
│
├── documents/          # Static knowledge sources
│   ├── handbook.pdf
│   ├── policies.md
│   └── notes.txt
│
├── loaders/            # Format-specific document loaders
├── services/           # External service clients (mocked)
├── chatbot.py          # Core logic and orchestration
├── cli.py              # Command-line interface
└── README.md
```

## How to Run the Chatbot

From the project root directory:

```bash
python cli.py
```
If everything is set up correctly, you will see:
```bash
📘 Chatbot ready.
Type 'exit' or 'quit' to stop.
```
The chatbot is now running.