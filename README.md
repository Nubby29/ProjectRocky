# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, and improve over time.

## Current milestone

Rocky 0.4 — Verification

Rocky can now:
- detect whether a subject is already known;
- collect explicitly supplied learning evidence;
- keep evidence separate from verified knowledge;
- compare multiple supplied sources deterministically;
- mark agreeing evidence as VERIFIED;
- keep single-source evidence UNVERIFIED;
- refuse to promote conflicting sources to verified knowledge;
- persist verified facts with their source labels.

### Run

    python -m rocky.main

### Example

    learn Python: Python is a programming language.
    verify Python
    learn Python: Python is a programming language.
    verify Python
    ask Python

The first verification remains UNVERIFIED because Rocky has only one source. After a second agreeing source is supplied, Rocky marks the knowledge VERIFIED and stores it as a fact. If supplied sources disagree, Rocky reports CONFLICT and does not promote the information to verified knowledge.

This phase uses deterministic comparison only. It does not browse the web, decide whether a real-world source is authoritative, or resolve semantic disagreements. Those capabilities belong to later research and reasoning milestones.
