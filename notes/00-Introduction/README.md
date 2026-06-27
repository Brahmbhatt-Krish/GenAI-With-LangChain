# Introduction to Generative AI & LangChain

## What is Generative AI?

Generative AI (GenAI) is a class of AI systems that generate new content — text, images, audio, video, code, or structured data — rather than only classifying or predicting on existing data.

Examples of model families: GPT, Gemini, Claude, Llama, Mistral.

## What is an LLM?

A Large Language Model (LLM) is a deep learning model trained on large-scale text data to learn grammar, facts, reasoning patterns, and context. At inference time, it predicts the next most probable token given prior context.

```
Input:  "The capital of France is ___"
Output: "Paris"
```

## Why LangChain?

Calling an LLM directly is sufficient for single-shot tasks, but production AI applications typically need to:

- Maintain conversation state across turns
- Retrieve and ground responses in external data (PDFs, databases, APIs)
- Orchestrate multi-step workflows
- Call external tools
- Return structured, validated output

Building this manually for every project doesn't scale. **LangChain** is an open-source framework that provides reusable, composable components for these concerns, so applications can be built consistently rather than from scratch each time.

## Core Components

| Component | Responsibility |
|---|---|
| **Models** | Interface to LLMs, Chat Models, and Embedding Models |
| **Prompts** | Define and structure how instructions are sent to a model |
| **Chains** | Compose multiple steps/operations into a single workflow |
| **Indexes** | Connect external knowledge sources (loaders, splitters, vector stores, retrievers) |
| **Memory** | Persist conversation state across an inherently stateless LLM API |
| **Agents** | Add reasoning + tool-use for multi-step, autonomous task execution |

```
                LangChain
                    │
 ┌──────────────────┼──────────────────┐
 │                  │                  │
Models           Prompts           Chains
 │                  │                  │
Indexes           Memory             Agents
```

## Typical Application Flow

```
User Input → Prompt Template → Model → (Memory / Tools, optional) → Structured Output → Response
```

## Stateless by Default

LLM API calls don't retain context between calls. Without memory:

```
User: My name is Krish.
User: What's my name?
AI:   I don't know.
```

With memory layered in via LangChain, conversation context persists across turns.

## Where This Is Used in Practice

- Chatbots and customer support assistants
- RAG (Retrieval-Augmented Generation) systems
- Document/PDF Q&A
- AI research and coding assistants
- Multi-agent systems

## Key Takeaways

- GenAI generates content; it doesn't just analyze it.
- LLMs operate via next-token prediction over learned context.
- LangChain's value is composability — modular components over custom glue code per project.
- Six core building blocks: **Models, Prompts, Chains, Indexes, Memory, Agents.**

---
**Next:** [01 — Models](../01-models/notes.md)