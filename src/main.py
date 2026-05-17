"""
Entry point. Orchestrates the full pipeline:
fetch → summarize → format → deliver

Usage:
  python src/main.py              # full run — fetches, summarizes, sends
  python src/main.py --dry-run    # prints bulletin to terminal, skips WhatsApp
"""

import sys
from dotenv import load_dotenv
load_dotenv()

from fetcher import fetch_all
from summarizer import summarize
from formatter import format_bulletin
from delivery import send_whatsapp


def run(dry_run: bool = False):
    print("[main] Fetching stories...")
    raw = fetch_all()

    print("\n[main] Summarizing with Claude...")
    bulletin = summarize(raw)

    print("[main] Formatting bulletin...")
    message = format_bulletin(bulletin)

    print("\n" + "─" * 50)
    print(message)
    print("─" * 50 + "\n")

    if dry_run:
        print("[main] Dry run — bulletin NOT sent to WhatsApp.")
    else:
        print("[main] Sending to WhatsApp...")
        send_whatsapp(message)
        print("[main] Done.")


if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    run(dry_run=dry_run)
