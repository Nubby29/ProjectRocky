# Project Rocky

A small, growable AI designed to detect what it does not know, learn new information, verify it, remember it, improve over time, and perform controlled actions.

## Rocky 1.0 — Growing Brain

Rocky now has an optional local language-model brain through an Ollama-compatible API. The model is a generation/reasoning layer; Rocky's persistent memory, verification, self-evaluation, skills, and tools remain separate subsystems.

Default model: `llama3.2:3b`
Default endpoint: `http://127.0.0.1:11434`

Override with environment variables:

    $env:ROCKY_MODEL="your-model"
    $env:ROCKY_MODEL_URL="http://127.0.0.1:11434"

Run:

    python -m rocky.main

Then use:

    chat <message>

Rocky sends the message plus a compact memory context to the local model. Model responses are recorded as `conversation` experiences, but the model does **not** automatically write new facts into verified memory.

If the local model is unavailable, Rocky reports that clearly instead of pretending it generated an answer.

This phase does not introduce autonomous web research, automatic fact promotion, model training, or arbitrary code execution.
