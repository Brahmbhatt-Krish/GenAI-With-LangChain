# Structured Output

LLMs naturally generate unstructured text. That's fine for conversation, but production systems need consistent, machine-readable data — not text that has to be regex-parsed and breaks on every wording change.

## The Problem

Asking an LLM to "summarize this review and give its sentiment" can return:

```text
The product is excellent.
Overall sentiment is positive.
Pros: Fast, Reliable
Cons: Expensive
```

Readable by a human, fragile for code — where does the summary end, which lines are pros, what if phrasing shifts? Every variation needs new parsing logic.

## The Fix: Schema-Driven Generation

Instead, define the shape of the response upfront and have the model fill it in:

```json
{
  "summary": "Excellent product with reliable performance.",
  "sentiment": "positive",
  "pros": ["Fast", "Reliable"],
  "cons": ["Expensive"]
}
```

Every field now has a predictable location — trivial for an application to consume.

**Common use cases:** AI agents, information/resume extraction, document processing, function calling, API integrations — essentially anywhere a program (not a human) consumes the output.

## How LangChain Does It

```
User Prompt → Chat Model + Schema → Structured Response
```

LangChain injects the schema into the prompt as generation instructions, and the model produces output conforming to it.

## Defining Schemas: Two Approaches

```
Structured Output
       │
   ┌───┴────┐
TypedDict  Pydantic
```

### TypedDict
A typed dictionary — defines expected keys and types, nothing more.

```python
from typing import TypedDict

class Review(TypedDict):
    summary: str
    sentiment: str
```

```python
structured_model = model.with_structured_output(Review)
response = structured_model.invoke(prompt)
# type(response) -> dict
```

**`Annotated`** lets you attach a natural-language description to a field, which LangChain feeds into the prompt to improve output quality:

```python
summary: Annotated[str, "A concise summary of the review"]
```

Other useful typing constructs:
- `Literal["positive", "negative"]` — restrict output to a fixed set of values
- `Optional[list[str]]` — field may be absent / `None`

**Limitation:** TypedDict defines structure but performs **no validation**. If the model returns `"sentiment": "pos"` instead of `"positive"`, nothing catches it — it silently flows downstream.

### Pydantic
A data validation library — type checking, validation, parsing, and serialization, returning real Python objects instead of plain dicts.

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str
    age: Optional[int]
    email: EmailStr
    marks: float = Field(gt=0, lt=100, description="Student's marks")
```

```python
student = Student(**data)  # validated immediately
```

At creation time, Pydantic checks required fields exist, types match, formats (e.g. email) are valid, and constraints are satisfied. Invalid data raises a `ValidationError` immediately rather than propagating silently.

`Field()` also lets you attach descriptions, defaults, and min/max constraints — these get surfaced to the model via the prompt too, the same way `Annotated` does for TypedDict.

Pydantic also generates a JSON Schema automatically (`Model.model_json_schema()`), which LangChain uses directly when a provider expects schema-based structured generation.

## End-to-End Flow

```
User Prompt → Schema → LangChain → Chat Model → Raw Response → Pydantic Validation → Validated Object
```

## TypedDict vs Pydantic

| Feature | TypedDict | Pydantic |
|---|---|---|
| Defines structure | ✅ | ✅ |
| Runtime validation | ❌ | ✅ |
| Type enforcement | ❌ | ✅ |
| Default values / constraints | ❌ | ✅ |
| JSON Schema support | Limited | ✅ |
| Production-ready | Moderate | High |

**Use TypedDict** for prototyping, learning, or simple schemas where validation isn't critical.
**Use Pydantic** for APIs, agents, RAG pipelines, function calling, and anything production — validation prevents bad model output from silently propagating into the rest of the system.

## Best Practices

- Always define an explicit schema — never rely on free-text parsing for machine-consumed output.
- Prefer Chat Models over plain LLMs for structured generation.
- Use `Annotated`/`Field()` descriptions — they materially improve generation accuracy.
- Use `Literal` for closed-set values, `Optional` only when a field can legitimately be missing.
- Validate every model response before it reaches downstream systems.
- Default to Pydantic in production.

## Key Takeaways

- LLMs generate unstructured text by default; schemas make output predictable and machine-readable.
- TypedDict = lightweight structure, no validation.
- Pydantic = structure + runtime validation + JSON Schema — the production default.
- Field descriptions (`Annotated` / `Field()`) double as both documentation and prompt-quality improvements.

---
**Previous:** [06 — Agents](../06-agents/notes.md)