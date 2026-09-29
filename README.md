# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, and improve over time.

## Current milestone

Rocky 0.7 — Doing

Rocky now adds a reusable skill layer on top of its learning, verification, and memory systems. Skills are deterministic actions with a name, description, and executable handler.

Built-in skills:
- **echo** — returns text unchanged;
- **uppercase** — converts text to uppercase;
- **lowercase** — converts text to lowercase;
- **length** — counts characters.

### Run

    python -m rocky.main

### Examples

    skills
    do echo: hello Rocky
    do uppercase: rocky can do things
    do length: hello
    memories

Every skill execution is recorded as an episodic experience. The registry is intentionally small and deterministic so future phases can add learned skills, tools, and safer action policies without coupling them to the CLI.

Existing learning and verification commands remain available. This phase does not execute arbitrary Python, shell commands, or external actions.
