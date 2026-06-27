# Models

Models are the execution engine of any GenAI application — they understand input, reason over context, and generate output. LangChain's Models module standardizes the interface across providers (OpenAI, Gemini, Anthropic, Ollama, etc.), so switching providers requires minimal code change.

```
User Input → Model → Generated Output
```

## Types of Models

```
                Models
                   │
      ┌────────────┼────────────┐
      ▼            ▼            ▼
    LLMs      Chat Models   Embedding Models
```

### 1. LLMs (Large Language Models)
Trained on massive text corpora to predict the next most probable token given prior context. Operate on plain text in, plain text out.

```
Input:  "The capital of Japan is"
Output: "Tokyo"
```

**Characteristics:** stateless by default, autocomplete-style generation.
**Use cases:** text generation, translation, summarization, code generation.

### 2. Chat Models
Instruction-tuned models built around conversational roles rather than raw text.

```python
[
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
]
```

**Advantages:** better instruction-following, multi-turn context, tool/function calling, structured outputs.
**Use cases:** chatbots, virtual assistants, coding assistants, agents.

> **Chat Models are the current industry standard** for production AI applications — LLMs are largely legacy at this point.

| Feature | LLM | Chat Model |
|---|---|---|
| Input | Plain text | Structured messages |
| Conversation support | ❌ | ✅ |
| Tool / function calling | ❌ | ✅ |
| Best for | Text generation | Conversational AI / agents |

### 3. Embedding Models
Don't generate text — they convert text into dense numerical vectors that capture semantic meaning. Semantically similar text produces vectors that sit close together in vector space.

```
"I love programming" → [0.91, -0.22, 0.54, ...]
```

**Use cases:** semantic search, RAG, recommendation systems, similarity/duplicate detection, clustering.

## Key Model Parameters

### Temperature
Controls randomness/creativity of output.

| Temperature | Behavior | Best for |
|---|---|---|
| 0.0 – 0.2 | Deterministic, accurate | Coding, SQL, APIs, RAG |
| 0.5 | Balanced | General-purpose |
| 0.8 – 1.0+ | Creative, diverse, random | Brainstorming, copywriting, storytelling |

### Max Tokens
Caps the length of generated output. Higher limits → longer responses, but more latency and cost.

### Top-P (Nucleus Sampling)
Restricts token selection to the most probable subset. Lower = focused output, higher = more diverse output.

## Proprietary vs Open-Source

| | Proprietary (GPT-4, Gemini, Claude) | Open-Source (Llama, Mistral, Gemma, Qwen) |
|---|---|---|
| Access | Hosted API | Self-hosted / local |
| Pros | High performance, managed infra, frequent updates | No vendor lock-in, privacy, fine-tunable |
| Cons | Cost, internet dependency, vendor lock-in | Needs hardware, ops overhead, slower on consumer devices |

## LangChain's Provider Abstraction

```
            LangChain
                │
 ┌──────────────┼──────────────┐
 ▼              ▼              ▼
OpenAI       Gemini       Ollama
```

Application logic stays the same regardless of which provider sits underneath — swap the model, not the codebase.

## Choosing the Right Model

| Task | Recommended |
|---|---|
| Chatbot / Agent | Chat Model |
| RAG | Chat Model + Embeddings |
| Semantic Search / Recommendations | Embedding Model |
| Code Generation | Chat Model |
| Translation | LLM / Chat Model |

## Best Practices

- Default to Chat Models for new applications.
- Use Embedding Models only for semantic tasks, never text generation.
- Keep temperature low for deterministic/factual tasks; raise it only for creative generation.
- Pick models on latency, cost, context window, and accuracy — not just benchmark leaderboard position.
- Design model-agnostic, leaning on LangChain's abstraction layer to avoid vendor lock-in.

## Key Takeaways

- Models are the core execution engine; LangChain standardizes LLMs, Chat Models, and Embedding Models behind one interface.
- Chat Models are the production default today.
- Embeddings convert text to vectors for semantic tasks — not generation.
- Temperature trades off determinism vs. creativity.
- LangChain's abstraction layer makes applications portable across providers.

---
**Next:** [02 — Prompt Engineering](../02-prompt-engineering/notes.md)