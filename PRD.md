# PRD: Sneha's Daily Bulletin

---

## 1. Overview

**Product Name:** Sneha's Daily Bulletin *(working title)*

**One-liner:** A fully automated daily news digest covering politics, AI, and the most important world events — summarized by AI and delivered to WhatsApp every evening at 9 PM IST.

**Problem Statement:**
News is fragmented across Instagram, YouTube, and dozens of channels with no single go-to place. The result is inconsistent consumption and a persistent feeling of being out of the loop. Too many categories make it worse — you open it for a few days and stop.

**Core Insight:**
A focused, short bulletin you actually read every day is worth more than a comprehensive one you abandon in a week. Three sections. Every day. WhatsApp.

---

## 2. Users

### Primary — The Editor (Sneha Amruth)
- Receives the bulletin daily
- Sets the editorial taste — her curation, her preferences
- Shares with family and friends on her own terms

### Secondary — Family & Friends
- Receive the bulletin via WhatsApp forward
- No setup, no preferences, no onboarding required
- Take it or leave it

---

## 3. Goals

| Goal | Description |
|---|---|
| **Daily habit** | Short enough to read every single day without losing interest |
| **Informed citizen** | Up to date on global politics, India, US, geopolitics, economic policy |
| **Professionally sharp** | Current on AI and tech industry developments |
| **Nothing critical missed** | Worth Knowing catches everything important outside the two main sections |
| **Zero effort** | Arrives at 9 PM IST — no searching, no opening apps |
| **Shareable** | Clean enough to forward on WhatsApp |

---

## 4. Non-Goals

- Not a breaking news alert system — strictly a daily digest at 9 PM
- Not personalized per recipient — one bulletin, Sneha's taste
- Not a full article — headline + one line of context only
- Not a web or mobile app — WhatsApp only
- Not covering sports, entertainment, celebrity news

---

## 5. Bulletin Structure

```
📌 TOP STORIES
   The 2-3 most important things today — regardless of category.
   If you read nothing else, read this.

🏛️ POLITICS
   • India politics
   • US politics
   • Geopolitics (wars, treaties, international relations)
   • Economic policy (budgets, trade wars, inflation, markets)

🤖 AI & TECH
   • Industry (product launches, funding, big tech moves)
   • Research & Dev (papers, tools, breakthroughs, engineering)
   Both blended into one section.

📎 WORTH KNOWING
   Important things happening in the world that don't fall
   into Politics or AI. The catch-all. Nothing major slips through.
```

**Per story format:**
```
• [Headline] — One sentence of context explaining what happened
  and why it matters.
```

**Example:**
```
• India and Pakistan agree to ceasefire along LoC — First formal
  de-escalation in 3 years following back-channel diplomatic talks
  brokered by the UAE.
```

---

## 6. Sources

### Politics
| Source | Format | Why |
|---|---|---|
| Reuters | RSS | Global gold standard, factual |
| BBC News | RSS | Broad global + India coverage |
| The Print | RSS | India politics, analytical |
| NDTV | RSS | India breaking political news |
| The Hindu | RSS | India politics, authoritative |
| r/worldnews | Reddit API | Community-validated global importance |
| r/india | Reddit API | India-specific signal |
| r/geopolitics | Reddit API | International relations discussion |
| r/economics | Reddit API | Economic policy discussion |

### AI & Tech
| Source | Format | Why |
|---|---|---|
| TechCrunch | RSS | Industry — launches, funding |
| The Verge | RSS | Industry — big tech, consumer AI |
| Wired | RSS | AI policy, tech culture |
| VentureBeat | RSS | AI-focused business news |
| MIT Technology Review | RSS | Deep AI research + policy |
| devurls.com | RSS | Developer — pre-curated dev news |
| lobste.rs | RSS | Developer — high-signal engineering |
| Hacker News (top) | API | Developer gold standard |
| r/MachineLearning | Reddit API | AI research, papers |
| r/artificial | Reddit API | General AI news |
| r/programming | Reddit API | Dev tools and languages |

### Worth Knowing
| Source | Format | Why |
|---|---|---|
| Reuters | RSS | Catches important non-political stories |
| BBC News | RSS | Science, health, major world events |
| r/worldnews | Reddit API | Upvoted = community says it matters |

---

## 7. Delivery

| Parameter | Value |
|---|---|
| **Channel** | WhatsApp |
| **Time** | 9:00 PM IST, every day |
| **Frequency** | Daily, 7 days a week |
| **Format** | Plain text with emoji section headers |
| **Length** | 2-3 stories per section — readable in under 5 minutes |
| **Breaking news** | Out of scope for v1 |

---

## 8. System Flow

```
6:00 PM IST — Pipeline starts
      |
      ▼
Fetch all RSS feeds + Reddit API
(Top posts from past 24 hours, sorted by upvotes)
      |
      ▼
Deduplicate
(Same story from multiple sources → keep best version)
      |
      ▼
AI Summarization (Claude API)
- Assign each story to correct section
- Generate headline + one-line context
- Select Top Stories (2-3 most important across all sections)
- Overflow anything important → Worth Knowing
      |
      ▼
Format for WhatsApp
(Emoji headers, clean bullet points, mobile-readable)
      |
      ▼
9:00 PM IST — Delivered to WhatsApp
```

---

## 9. Technical Architecture

| Layer | Choice | Reason |
|---|---|---|
| **Language** | Python | Best ecosystem for this use case |
| **Scheduler** | GitHub Actions (cron) | Free, reliable, no server needed |
| **RSS Parsing** | `feedparser` | Simple, well-maintained Python library |
| **Reddit Data** | Reddit API via PRAW | Free, official, reliable |
| **AI Summarization** | Claude API (claude-sonnet-4-6) | Best instruction-following and tone control |
| **WhatsApp Delivery** | Twilio WhatsApp API | Easiest programmatic WhatsApp sending |
| **Hosting** | GitHub Actions | Runs on schedule, zero infrastructure cost |

---

## 10. Success Metrics

| Metric | Target | Why |
|---|---|---|
| **Delivery reliability** | Arrives at 9 PM IST every day | Core promise |
| **Read rate** | Sneha reads it within 30 mins of delivery daily | It's actually useful |
| **Top Stories accuracy** | The 2-3 stories feel genuinely important in hindsight | AI curation is working |
| **Section coverage** | Every section has at least 1 story every day | No section ever runs dry |
| **Forward rate** | Forwarded to at least one person | It's shareable |

---

## 11. Open Questions

| Question | Options | Impact |
|---|---|---|
| **WhatsApp API** | Twilio vs Meta Business API directly | Cost vs. setup complexity |
| **Source goes down** | Skip source vs. fallback source | Pipeline reliability |
| **No news in a section** | Skip section vs. pull from previous day | Bulletin completeness |
| **Top Stories overlap** | What if Top Stories duplicates a section story? | Formatting clarity |
| **Prompt tuning** | How much editorial control over AI tone? | Bulletin personality |

---

## 12. Milestones

| Phase | Scope |
|---|---|
| **Phase 1 — Data Pipeline** | Fetch RSS + Reddit, parse, deduplicate, raw data works reliably |
| **Phase 2 — Summarization** | Claude API integration, section assignment, one-line summaries |
| **Phase 3 — Formatting** | WhatsApp-ready output, clean on mobile, emoji headers |
| **Phase 4 — Delivery** | Twilio integration, 9 PM IST trigger working end-to-end |
| **Phase 5 — Reliability** | Error handling, source fallbacks, monitoring |
| **Phase 6 — Tuning** | Refine prompts based on real bulletin quality over first 2 weeks |
