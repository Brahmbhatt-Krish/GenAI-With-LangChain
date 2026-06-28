from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
import os

load_dotenv()  # Load environment variables from .env file

# Initialize the HuggingFace inference endpoint with the target model
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
)

# Wrap the endpoint in ChatHuggingFace to support chat-style message formatting
# (required for .with_structured_output() to function correctly)
model = ChatHuggingFace(llm=llm)


#PART 1: Basic TypedDict Schema

# Define the output schema — the model must return a dict with these exact fields
class Review(TypedDict):
    summary: str    # plain text summary of the review
    sentiment: str  # overall sentiment expressed

# Bind the schema to the model — LangChain auto-generates a system prompt
# behind the scenes that instructs the model to return output in this structure
structured_model = model.with_structured_output(Review)

res = structured_model.invoke("The product exceeded my expectations with its quality and performance. It's easy to use, offers great value for money, and I would definitely recommend it.")

print(res)          # {'summary': '...', 'sentiment': '...'}
print(type(res))    # <class 'dict'> — TypedDict produces a plain Python dict


#  PART 2: Annotated TypedDict 
#
# Annotated[type, "description"] attaches a plain-English hint to each field.
# LangChain includes these hints in the generated prompt so the model knows
# the exact expected format or range of values for each field.
#
# Supporting types used:
#   Literal["a", "b"]  — restricts output to a fixed set of allowed values
#   Optional[X]        — field may be None if no relevant content is found
#   list[str]          — expects a list of string items

class Review_one(TypedDict):
    summary:Annotated[str,"A brief summery of the review"]
    sentiment:Annotated[Literal["pos,neg"],"Return sentiment of the review with negative positive or netural"]
    pros:Annotated[Optional[list[str]],"Write down all the pros inside a list" ]
    cons:Annotated[Optional[list[str]],"Write down all the cons inside a list"]

structured_model1 = model.with_structured_output(Review_one)

res1 = structured_model1.invoke('''
I've been using this product for a while, and overall it's been a positive experience. The build quality is solid, the performance is reliable, and it's easy to use right out of the box. One of its biggest strengths is that it delivers exactly what it promises without unnecessary complexity.

On the downside, the battery life could be better, and the price feels slightly higher than some competing products with similar features. Despite these minor drawbacks, I'm satisfied with the purchase because the overall quality and performance make it worth considering. I would recommend it to anyone looking for a dependable product.

''')

print(res1)


# LIMITATION 
# TypedDict defines structure only — it does NOT validate values at runtime.
# The model could return sentiment as "positive" instead of "pos" and no error
# would be raised. For runtime validation and strict type enforcement, use Pydantic.