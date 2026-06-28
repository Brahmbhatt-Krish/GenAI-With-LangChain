from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from dotenv import load_dotenv
from typing import Optional, Literal
from pydantic import BaseModel, Field
import os

load_dotenv()  # Load environment variables from the .env file

# Initialize the HuggingFace inference endpoint with the target model
llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-72B-Instruct",
    task="text-generation",
    huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
)

# Wrap the endpoint in ChatHuggingFace to enable chat-style prompting
# and structured output generation
model = ChatHuggingFace(llm=llm)


# 
# PART 3: Structured Output with Pydantic
# 
#
# Pydantic extends basic schema definition by providing runtime
# validation and type enforcement. Unlike TypedDict, it verifies that
# the generated output strictly conforms to the declared schema.
#
# Field(...) attaches descriptive metadata to each attribute. LangChain
# incorporates these descriptions into the generated prompt, improving
# the model's ability to produce correctly formatted responses.
#
# Supported types used:
#   Literal["pos", "neg"]  → restricts values to a predefined set
#   Optional[X]            → field may be omitted or set to None
#   list[str]              → expects a list of string values


class Review_one(BaseModel):
    summery: list[str] = Field(
        description="A concise summary of the product review."
    )

    sentiment: Literal["pos", "neg"] = Field(
        description="Overall sentiment expressed in the review."
    )

    pros: Optional[list[str]] = Field(
        default=None,
        description="List of positive aspects mentioned in the review."
    )

    cons: Optional[list[str]] = Field(
        default=None,
        description="List of negative aspects mentioned in the review."
    )


# LangChain's with_structured_output() expects a JSON Schema when used
# with HuggingFace chat models. model_json_schema() converts the
# Pydantic model into the required JSON Schema representation.

structured_model1 = model.with_structured_output(
    Review_one.model_json_schema()
)


# Generate a structured response from the input review. The model
# returns a standard Python dictionary that follows the provided schema.

raw_res = structured_model1.invoke(
    '''
I've been using this product for a while, and overall it's been a positive experience. The build quality is solid, the performance is reliable, and it's easy to use right out of the box. One of its biggest strengths is that it delivers exactly what it promises without unnecessary complexity.

On the downside, the battery life could be better, and the price feels slightly higher than some competing products with similar features. Despite these minor drawbacks, I'm satisfied with the purchase because the overall quality and performance make it worth considering. I would recommend it to anyone looking for a dependable product.
'''
)


# Convert the returned dictionary into a Pydantic model instance.
#
# During object creation, Pydantic validates:
#    Required fields are present
#    Data types match the schema
#    Literal values satisfy the allowed constraints
#
# If validation fails, Pydantic raises a ValidationError, ensuring that
# invalid outputs are detected immediately.

res1 = Review_one(**raw_res)


# Display the validated Pydantic model instance
print(res1)

# The resulting object is an instance of the Pydantic model rather than
# a plain Python dictionary.
print("\nOutput type:", type(res1))