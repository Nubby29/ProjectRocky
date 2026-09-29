# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, improve over time, and perform controlled actions.

## Current milestone

Rocky 0.9 — Self-Evaluation

Rocky can now inspect its own stored knowledge before answering. Self-evaluation uses explicit memory state rather than pretending to measure real-world truth.

### Knowledge states

- **VERIFIED (1.00)** — an explicitly verified fact is stored;
- **UNVERIFIED (0.50)** — evidence exists but is not verified;
- **LEGACY (0.25)** — older fact exists without verification metadata;
- **UNKNOWN (0.00)** — no stored knowledge or evidence;
- **CONFLICT (0.00)** — stored sources disagree.

These values are deterministic memory-status signals, not probabilities that a statement is objectively true.

### Run

    python -m rocky.main

### Examples

    evaluate Python
    evaluate Java
    ask Python

The `ask` flow now checks self-evaluation and refuses to present conflicting evidence as verified knowledge. Evaluation events are recorded in episodic memory.

Existing learning, verification, memory, skills, and controlled tools remain available.

## Safety boundary

Rocky still does not execute arbitrary Python or shell commands, and it does not claim that a confidence value guarantees real-world truth.
