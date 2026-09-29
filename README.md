# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, improve over time, and perform controlled actions.

## Current milestone

Rocky 0.8 — Tools

Rocky now has a controlled tool layer alongside its reusable skills.

Built-in tools:
- **calculate** — safely evaluates numeric arithmetic using an allowlisted AST;
- **read_file** — reads a UTF-8 text file from a supplied path.

### Run

    python -m rocky.main

### Examples

    tools
    use calculate: 25 * 4 + 10
    use read_file: notes.txt
    memories

Tool executions are recorded as episodic experiences. Tools are explicitly registered and deterministic. The calculator never executes Python code, and this phase does not provide arbitrary shell/Python execution or web access.

Existing learning, verification, memory, and skill commands remain available.
