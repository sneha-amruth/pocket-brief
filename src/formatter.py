"""
Formats the structured bulletin dict into a clean WhatsApp message.
"""

from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))


def format_bulletin(bulletin: dict) -> str:
    today = datetime.now(IST).strftime("%A, %d %B %Y")
    lines = [
        f"*Sneha's Daily Bulletin*",
        f"_{today}_",
        "",
    ]

    def add_section(emoji: str, title: str, stories: list[dict]):
        if not stories:
            return
        lines.append(f"{emoji} *{title}*")
        for story in stories:
            lines.append(f"• {story['headline']} — {story['context']}")
        lines.append("")

    add_section("📌", "TOP STORIES", bulletin.get("top_stories", []))
    add_section("🏛️", "POLITICS", bulletin.get("politics", []))
    add_section("🤖", "AI & TECH", bulletin.get("ai_tech", []))
    add_section("📎", "WORTH KNOWING", bulletin.get("worth_knowing", []))

    return "\n".join(lines).strip()
