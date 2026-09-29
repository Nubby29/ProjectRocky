"""Command-line entry point for Project Rocky 1.5."""

from .brain.memory_brain import MemoryBrain
from .brain.model import LocalModelBrain
from .config import load_settings
from .learning.learner import Learner
from .logging_config import configure_logging
from .memory.store import MemoryStore
from .reasoning.self_evaluator import SelfEvaluator
from .skills.builtin import register_builtin_skills
from .skills.registry import SkillRegistry
from .tools.builtin import register_builtin_tools
from .tools.registry import ToolRegistry
from .verification.verifier import Verifier


def parse_learn_command(command: str) -> tuple[str, str, str]:
    subject_and_source, source_text = command.split(":", 1)
    subject_and_source, source_text = subject_and_source.strip(), source_text.strip()
    source = "user-supplied"
    if subject_and_source.endswith("]") and "[" in subject_and_source:
        subject, source_part = subject_and_source.rsplit("[", 1)
        subject, source = subject.strip(), source_part[:-1].strip()
        if not subject or not source: raise ValueError("learn format must be: learn <subject> [source]: <source text>")
        return subject, source_text, source
    return subject_and_source, source_text, source


def build_model_context(memory: MemoryStore) -> str:
    """Build an explicit knowledge-status context for Rocky's language model."""
    facts = memory.load().get("facts", [])
    if not facts:
        return "No stored memory is available."

    lines = []
    for fact in facts:
        status = fact.get("verification", "LEGACY").upper()
        lines.append(f"- [{status}] {fact.get('subject', '')}: {fact.get('text', '')}")
    return "\n".join(lines)


def print_memory(memory: MemoryStore) -> None:
    facts, experiences = memory.load()["facts"], memory.find_experiences()
    print(f"Rocky: Memory contains {len(facts)} fact(s) and {len(experiences)} experience(s).")
    for fact in facts: print(f"  FACT [{fact.get('verification','LEGACY')}] {fact['subject']}: {fact['text']}")
    for experience in experiences[-10:]: print(f"  EXPERIENCE [{experience.get('kind','unknown')}] {experience.get('timestamp','')}: {experience.get('text','')}")


def main() -> None:
    settings=load_settings(); logger=configure_logging(settings.log_file); memory=MemoryStore(settings.memory_file); memory.load()
    brain=MemoryBrain(memory); learner=Learner(memory); verifier=Verifier(memory); evaluator=SelfEvaluator(memory)
    skills=SkillRegistry(); register_builtin_skills(skills)
    tools=ToolRegistry(); register_builtin_tools(tools); model_brain=LocalModelBrain(settings.model_name, settings.model_url)
    logger.info("Rocky started")
    print("Project Rocky 1.5 — Multimodal")
    print("I can learn, verify, remember, evaluate my knowledge, perform skills, use controlled tools, and chat with text or images through local models.")
    print("Commands: chat <message> | chat-image <image-path>: <message> | remember <subject>: <fact> | recall <subject> | learn <subject> [source]: <source text> | verify <subject> | evaluate <subject> | ask <subject> | skills | do <skill>: <input> | tools | use <tool>: <input> | experience <kind>: <text> | memories | forget <subject> | exit")
    while True:
        try: user_input=input("You: ").strip()
        except (EOFError,KeyboardInterrupt): print(); break
        if user_input.casefold() in {"exit","quit"}: break
        if not user_input: continue
        lower=user_input.casefold()
        try:
            if lower.startswith("chat-image ") and ":" in user_input:
                image_path, message = user_input[len("chat-image "):].rsplit(":", 1)
                context=build_model_context(memory)
                response=model_brain.chat_image(message, image_path, context)
                memory.add_experience("conversation", f"Vision model {response.model} analyzed {image_path.strip()}: {response.text}")
                print(f"Rocky: {response.text}")
            elif lower.startswith("chat "):
                message=user_input[len("chat "):].strip()
                context=build_model_context(memory)
                response=model_brain.chat(message, context)
                memory.add_experience("conversation", f"Model {response.model} answered: {response.text}")
                print(f"Rocky: {response.text}")
            elif lower.startswith("remember ") and ":" in user_input:
                subject,fact=user_input[len("remember "):].split(":",1); response=brain.remember(subject,fact); memory.add_experience("memory",f"Explicitly remembered fact about {subject.strip()}."); print(f"Rocky: {response}")
            elif lower.startswith("recall "): print(f"Rocky: {brain.recall(user_input[len('recall '):].strip())}")
            elif lower.startswith("learn ") and ":" in user_input:
                subject,text,source=parse_learn_command(user_input[len("learn "):]); print(f"Rocky: {learner.learn(subject,text,source).message}")
            elif lower.startswith("verify "): print(f"Rocky: {verifier.verify(user_input[len('verify '):].strip()).message}")
            elif lower.startswith("evaluate "):
                result=evaluator.evaluate(user_input[len("evaluate "):].strip())
                print(f"Rocky: {result.subject} — status={result.status}, confidence={result.confidence:.2f}. {result.reason}")
                memory.add_experience("self-evaluation", f"Evaluated {result.subject}: {result.status} ({result.confidence:.2f}).")
            elif lower.startswith("ask "):
                subject=user_input[len("ask "):].strip(); evaluation=evaluator.evaluate(subject); result=learner.learn_if_unknown(subject)
                if result.status=="UNKNOWN": print(f"Rocky: {result.message}\nRocky: Provide a source with: learn <subject> [source]: <source text>")
                elif evaluation.status=="CONFLICT": print(f"Rocky: I found conflicting information about {subject}, so I will not present it as verified knowledge.")
                else: print(f"Rocky: {brain.recall(subject)}")
            elif lower=="skills":
                print("Rocky: Available skills:"); [print(f"  {x.name}: {x.description}") for x in skills.list()]
            elif lower.startswith("do ") and ":" in user_input:
                name,arg=user_input[len("do "):].split(":",1); result=skills.run(name,arg); memory.add_experience("skill",f"Executed skill {name.strip()}: {arg.strip()}"); print(f"Rocky: {result}")
            elif lower=="tools":
                print("Rocky: Available tools:"); [print(f"  {x.name}: {x.description}") for x in tools.list()]
            elif lower.startswith("use ") and ":" in user_input:
                name,arg=user_input[len("use "):].split(":",1); result=tools.run(name,arg); memory.add_experience("tool",f"Used tool {name.strip()}: {arg.strip()}"); print(f"Rocky: {result}")
            elif lower.startswith("experience ") and ":" in user_input:
                kind,text=user_input[len("experience "):].split(":",1); experience=memory.add_experience(kind,text); print(f"Rocky: I remembered that experience at {experience['timestamp']}.")
            elif lower=="memories": print_memory(memory)
            elif lower.startswith("forget "):
                subject=user_input[len("forget "):].strip()
                if memory.forget_fact(subject): memory.add_experience("memory",f"Forgot facts and learning evidence about {subject}."); print(f"Rocky: I forgot facts and learning evidence about {subject}.")
                else: print(f"Rocky: I had no facts or learning evidence to forget about {subject}.")
            else: print("Rocky: Use 'chat', 'remember', 'recall', 'learn', 'verify', 'evaluate', 'ask', 'skills', 'do', 'tools', 'use', 'experience', 'memories', or 'forget'.")
        except (ValueError,KeyError,RuntimeError) as exc: print(f"Rocky: I could not perform that operation: {exc}")


if __name__ == "__main__": main()
