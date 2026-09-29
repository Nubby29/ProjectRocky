# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, and improve over time.

## Current milestone

Rocky 0.6 — Remembering

Rocky now has three practical memory layers:
- **facts** — knowledge Rocky can recall;
- **experiences** — timestamped events describing what Rocky learned, verified, remembered, or forgot;
- **evidence** — source material that has not necessarily become verified knowledge.

Rocky can now:
- detect whether a subject is already known;
- collect explicitly supplied learning evidence;
- compare multiple supplied sources deterministically;
- mark agreeing evidence as VERIFIED;
- keep single-source evidence UNVERIFIED;
- refuse to promote conflicting sources to verified knowledge;
- persist verified facts with their source labels;
- record a timestamped learning and verification history;
- inspect its current memory with the memories command;
- store a manual experience with experience <kind>: <text>;
- forget a subject's facts and evidence with forget <subject>.

### Run

    python -m rocky.main

### Example

    learn Java [source-1]: Java is a programming language.
    learn Java [source-2]: Java is a programming language.
    verify Java
    ask Java
    memories

The memories command shows stored facts plus the most recent experiences. The forget command removes that subject's facts and evidence while leaving the experience history intact, so Rocky does not erase the fact that an earlier learning event occurred.

This phase still does not browse the web, choose authoritative sources, or perform semantic reasoning. The memory system is deliberately explicit and auditable so later autonomous learning can build on it safely.
