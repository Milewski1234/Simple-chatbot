# Simple Multi-Source Chatbot

## Overview
This project implements a lightweight chatbot capable of answering questions
from static documents (PDF, Markdown, Text) and dynamically retrieving
user-specific data from external systems.

The focus is architectural clarity, source-of-truth separation, and extensibility.

## Architecture
- CLI for interaction
- Query orchestrator for routing decisions
- Static document retriever
- Mocked external service for dynamic data

## Assumptions
- "Multi-modal" refers to heterogeneous document formats, not multimodal AI.
- No persistent state is owned by the system.
- External systems are authoritative for dynamic data.

## Design Decisions
- No database: the system owns no mutable state
- No LLM: semantic generation is unnecessary for the problem scope
- Explicit routing between static and dynamic sources

## Future Improvements
- Embedding-based retrieval for larger document sets
- LLM-based answer synthesis (optional)
- Real API integrations
- Caching and async execution

## Manual Testing

1. Start CLI
2. Ask static policy questions
3. Ask dynamic vacation balance question
4. Verify routing behavior
5. Verify graceful failures
