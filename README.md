# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, and improve over time.

## Current milestone

Rocky 0.3 — Learning

Rocky can now:
- detect whether a subject is already known;
- report an unknown subject;
- learn from an explicitly supplied source;
- store the learned information persistently;
- report KNOWN, UNKNOWN, or LEARNED states.

### Run

    python -m rocky.main

### Example

    ask Python
    learn Python: Python is a programming language.
    ask Python

The current learner intentionally requires a supplied source. It does not yet browse the web or automatically judge whether a source is trustworthy. Verification and external research are later milestones.
