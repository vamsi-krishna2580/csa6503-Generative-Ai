import time
import json

from llm_client import call_llm


PROMPT = """
You are an agricultural extension officer.

Write ONE advisory SMS under 160 characters in {language}.

Crop: {crop}
District: {district}
Soil: {soil}
Weather: {weather}

Rules:
- Give exactly one actionable instruction.
- No greetings.
- No emojis.
- Use plain, simple words.
- Do not invent weather conditions or crop facts.
- Do not give chemical dosage unless units are explicitly provided.
- Keep the advice relevant to the supplied crop and weather.
- Return ONLY the SMS text.
- Do not return JSON.
- Do not use quotation marks.
"""


FALLBACK_TEMPLATE = (
    "Monitor your {crop} crop closely based on current weather "
    "conditions in {district} and follow local agricultural guidance."
)


def clean_text(text):
    text = text.strip()

    # Handle JSON if model still returns it
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "sms" in data:
            return str(data["sms"]).strip()
    except Exception:
        pass

    return text.strip().strip('"')


def generate_advisory(
    params: dict,
    temperature: float = 0.3,
    top_p: float = 1.0
) -> dict:

    prompt = PROMPT.format(**params)

    for attempt in range(3):
        try:
            response = call_llm(
                prompt=prompt,
                temperature=temperature,
                top_p=top_p,
                max_tokens=120
            )

            text = clean_text(response["text"])

            return {
                "text": text,
                "latency_ms": response["latency_ms"],
                "prompt_tokens": response["prompt_tokens"],
                "completion_tokens": response["completion_tokens"],
                "attempts": attempt + 1,
                "fallback_used": False
            }

        except Exception as error:

            error_text = str(error)

            print(
                f"Attempt {attempt + 1} failed: {error_text}"
            )

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):
                wait_time = 2 ** attempt
                print(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                break

    return {
        "text": FALLBACK_TEMPLATE.format(**params),
        "latency_ms": 0,
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "attempts": 3,
        "fallback_used": True
    }