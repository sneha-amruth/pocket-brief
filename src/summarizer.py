"""
Takes raw stories from fetcher and uses Gemini to:
- Deduplicate stories covering the same event
- Assign each story to the correct section
- Generate a headline + one-line context per story
- Select 2-3 Top Stories across all sections
- Surface anything important that doesn't fit → Worth Knowing

Returns a structured bulletin dict ready for the formatter.
"""

from groq import Groq
import json
import os

SYSTEM_PROMPT = """You are the editor of Sneha's Daily Bulletin — a focused,
daily WhatsApp news digest. Your job is to cut through the noise and surface
only what genuinely matters.

Editorial taste:
- Clear, direct, no fluff
- Explain why something matters, not just what happened
- Prioritize impact over sensationalism
- No celebrity news, no sports, no entertainment

Tone: Informed friend summarizing the day, not a newscaster."""

USER_PROMPT_TEMPLATE = """Here are today's raw stories fetched from news sources.

POLITICS STORIES:
{politics}

AI & TECH STORIES:
{ai_tech}

WORTH KNOWING STORIES:
{worth_knowing}

Your tasks:
1. Deduplicate — if multiple stories cover the same event, pick the best version
2. Select the 2-3 most important stories of the day for TOP STORIES (any section)
3. For POLITICS: pick the 3-4 most important political stories (India, US, geopolitics, economic policy)
4. For AI & TECH: pick the 3-4 most important AI/tech stories (industry + developer blended)
5. For WORTH KNOWING: pick 1-2 important stories that don't fit politics or AI

For each story write:
- headline: short, clear, factual
- context: one sentence explaining what happened and why it matters

Return a JSON object in this exact format:
{{
  "top_stories": [
    {{"headline": "...", "context": "..."}}
  ],
  "politics": [
    {{"headline": "...", "context": "..."}}
  ],
  "ai_tech": [
    {{"headline": "...", "context": "..."}}
  ],
  "worth_knowing": [
    {{"headline": "...", "context": "..."}}
  ]
}}"""


def _format_stories_for_prompt(stories: list[dict]) -> str:
    if not stories:
        return "No stories fetched."
    lines = []
    for s in stories[:30]:  # cap to avoid token overflow
        lines.append(f"- {s['title']} ({s['source']})")
        if s.get("summary"):
            lines.append(f"  {s['summary'][:200]}")
    return "\n".join(lines)


def summarize(raw: dict[str, list[dict]]) -> dict:
    """Call Groq (Llama) to summarize and structure the bulletin."""
    client = Groq(api_key=os.environ["GROQ_API_KEY"])

    prompt = USER_PROMPT_TEMPLATE.format(
        politics=_format_stories_for_prompt(raw.get("politics", [])),
        ai_tech=_format_stories_for_prompt(raw.get("ai_tech", [])),
        worth_knowing=_format_stories_for_prompt(raw.get("worth_knowing", [])),
    )

    last_error = None
    for attempt in range(1, 4):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content.strip()

        # Strip markdown code fences if the model wraps the JSON
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"[summarizer] JSON parse failed (attempt {attempt}/3): {e}")
            last_error = e

    raise last_error
