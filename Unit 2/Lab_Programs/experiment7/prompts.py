def executive_prompt(text):
    return f"""
You are a senior business analyst.

Summarize the following production review meeting.

Requirements:
- Executive abstract for the Managing Director.
- Maximum 80 words.
- No technical jargon.
- Include only important business information.
- Do not invent facts, numbers, names or dates.

SOURCE:
{text}
"""


def action_prompt(text):
    return f"""
You are a meeting-minutes assistant.

Extract all action items from the source.

Requirements:
- Return only a bulleted list.
- Every item must contain:
  Owner:
  Task:
  Deadline:
- Do not invent owners, tasks or deadlines.
- Preserve factual accuracy.

SOURCE:
{text}
"""


def technical_prompt(text):
    return f"""
You are a technical production analyst.

Create a technical summary of the following meeting.

Requirements:
- Retain machine names exactly.
- Retain defect counts.
- Retain all important numerical values.
- Retain names and dates where relevant.
- Do not simplify technical information.
- Do not invent facts.

SOURCE:
{text}
"""


EMAIL_CONTEXT = """
ROLE:
You are a senior account manager at a precision-components manufacturer.

CONTEXT:
Client: Meridian Auto, a 7-year account.
Purchase Order: PO-4471.
Quantity: 400 units.
Original delivery date: 12 September.
Revised delivery date: 21 September.
Cause: sub-supplier casting failure.

TASK:
Write the delay notification email.

CONSTRAINTS:
- Maximum 150 words.
- Must explicitly state the revised delivery date.
- Must offer exactly one concrete remedy: partial early dispatch OR expedited freight.
- Must NOT admit legal liability.
- Must NOT reference penalty clauses.
- Must NOT apologise more than twice.
- Output Subject line followed by email body.
- No placeholders such as [Name].
"""


def email_prompt(tone):
    return EMAIL_CONTEXT + f"""

TONE:
{tone}

Generate the email now.
"""


PRODUCT_DATA = """
Product: EcoDrive IE5 Industrial Motor
Power rating: 15 kW
Efficiency class: IE5
Energy saving: up to 12% compared with conventional IE3 motors
Speed range: 500–3000 RPM
Voltage: 380–480 V
Protection: IP55
Use: industrial pumps, compressors and conveyor systems
Warranty: 3 years
"""


def content_prompt():
    return f"""
You are a B2B industrial marketing specialist.

Use ONLY the following product datasheet.
Do not invent specifications.

PRODUCT DATASHEET:
{PRODUCT_DATA}

Generate three coordinated outputs.

1. LINKEDIN POST
- B2B tone
- Specification-led
- 120 to 150 words

2. INSTAGRAM CAPTION
- Consumer-friendly tone
- Maximum 40 words
- Include hashtags

3. WEBSITE BLURB
- Exactly about 60 words
- Include these SEO keywords:
  energy-efficient industrial motor
  IE5 motor
  industrial motor efficiency

All three outputs must remain factually consistent.
Clearly label each section:
LINKEDIN:
INSTAGRAM:
WEBSITE:
"""


def ablation_prompt(remove_component):
    components = {
        "ROLE": """
ROLE:
You are a senior account manager at a precision-components manufacturer.
""",
        "CONTEXT": """
CONTEXT:
Client: Meridian Auto, a 7-year account.
Purchase Order: PO-4471.
Quantity: 400 units.
Original delivery date: 12 September.
Revised delivery date: 21 September.
Cause: sub-supplier casting failure.
""",
        "TONE": """
TONE:
Professional, accountable, not grovelling.
""",
        "WORD_COUNT": """
WORD-COUNT CONSTRAINT:
Maximum 150 words.
""",
        "OUTPUT_FORMAT": """
OUTPUT FORMAT:
Subject line followed by email body.
No placeholders such as [Name].
"""
    }

    prompt = ""

    for name, component in components.items():
        if name != remove_component:
            prompt += component

    prompt += """
TASK:
Write the delay notification email.

OTHER CONSTRAINTS:
- Must explicitly state the revised delivery date.
- Must offer exactly one concrete remedy: partial early dispatch OR expedited freight.
- Must NOT admit legal liability.
- Must NOT reference penalty clauses.
- Must NOT apologise more than twice.
"""

    return prompt