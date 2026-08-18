import os
import time

from google import genai
from google.genai import types


MODEL = "gemini-3.5-flash-lite"


def call_llm(
    prompt,
    temperature=0.2,
    top_p=1.0,
    max_tokens=150
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is not set."
        )

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        max_output_tokens=max_tokens,
        response_mime_type="application/json"
    )

    start = time.perf_counter()

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config
    )

    latency_ms = (
        time.perf_counter() - start
    ) * 1000

    usage = response.usage_metadata

    prompt_tokens = getattr(
        usage,
        "prompt_token_count",
        0
    ) or 0

    completion_tokens = getattr(
        usage,
        "candidates_token_count",
        0
    ) or 0

    return {
        "text": response.text.strip(),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "latency_ms": round(latency_ms, 2)
    }