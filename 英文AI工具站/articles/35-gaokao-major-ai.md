# A Teenager Asked Which Major to Pick. AI Refused to Answer. So I Built a Voting Tool.

**SEO Title:** Which College Majors Will Be Worth It in 4 Years? AI Refused to Answer — So I Built a Tool
**Meta Description:** I asked AI to pick the best major for my friend's child. It refused — and the reason it gave changed how I think about education decisions entirely. Here's what happened next.
**Slug:** which-college-major-ai-refused-answer-voting-tool
**Tags:** ai, education, side-hustle, building-in-public
**Category:** My AI Experiments

---

A friend passed me a question their teenager was wrestling with.

*"Which majors will still be good four years from now?"*

Simple question. Completely reasonable thing to ask. The kind of thing a 17-year-old in China has to figure out before the gaokao results come in and the clock starts ticking on a life decision.

I thought: I'll just ask AI.

I was wrong about how easy that would be.

---

## AI Refused to Just Pick a Major

I didn't expect that.

I fed the question to multiple AI models. I expected a list. "Computer science. Nursing. Electrical engineering. Done."

Instead, every model gave me some version of the same answer, and it was better than a list.

The one that stuck with me framed it like this: *picking a major based on what's "hot right now" is like buying a stock because it's already on the leaderboard.* By the time you graduate, the cycle has moved. The students who flooded into a field because it was booming in 2025 are graduating into a market that peaked in 2027.

The AI went further. It said there are two types of majors worth considering:

**Bottom-layer infrastructure** — mathematics, physics, computer science, electronic engineering. These are the grammar of how the modern world runs. No matter what the job market looks like in 2029, someone who understands the underlying logic of systems can apply it somewhere. These are the majors where the floor keeps getting higher, not lower.

**Hard-to-automate complexity** — fields where AI can assist but not replace: hands-on clinical care, hardware-meets-software engineering (robotics, semiconductors, smart grid), environmental and energy systems. These require physical presence, judgment under uncertainty, and expertise that can't be easily compressed into a model.

What it said to avoid: majors built around executing specific rules or tools rather than understanding underlying principles. Translation of routine documents. Basic bookkeeping. Template-driven design. These aren't bad careers. They're just careers where the floor is moving down, not up.

None of this was a list of majors. It was a framework for thinking about majors. Which is harder to use, and also more useful.

---

## I Found the Complete List: 816 Majors

The next problem: I didn't even know what all the options were.

China's Ministry of Education maintains an official directory of every accredited university major — all 816 of them across 14 academic categories. Philosophy to engineering. Nursing to police dog technology. The full range of human expertise, as defined by a government document.

I found it, downloaded it, and sat with it for a while.

816 is a lot. It's also clarifying. When you see the full map instead of just the familiar landmarks, you start to notice things. How many majors are variations on each other. How many are extremely specific to domestic policy priorities. How many would mean almost nothing outside of China.

---

## I Had It Translated Into English

My next thought: what do people *outside* China think about this?

The Chinese education system produces more university graduates than any other country on earth. The major choices made by millions of Chinese students every year ripple through global labor markets in ways that most people in other countries never think about.

I had every one of the 816 majors translated into English with their official international equivalents. Then I started wondering: if I put this list in front of English-speaking readers — people who've thought about careers and education from completely different systems — what would they vote for?

Would a developer in Germany pick the same majors as a nurse in the US? Would someone who works in finance see the same high-potential fields as a teacher?

I don't know. That's why I built the tool.

---

## The Voting Tool

It's on the tools page: **[China Major Ranking — Vote →](/tools/)**

The concept is simple. All 816 Chinese university majors, organized by academic category, with their English translations. You vote for the ones you think will be most valuable four years from now — from wherever you're sitting, in whatever field you work in.

The top 15 update in real time as votes come in.

I'm going to leave it running for five years.

Maybe the results will be obvious — CS and medicine at the top, obscure policy majors at the bottom. Maybe they'll be surprising. Maybe the gap between what Chinese students actually study and what international professionals would choose will be the story.

I genuinely don't know. And that's the point.

---

## Why Five Years

Because that's how long it takes to actually find out if an education decision was right.

The teenager who asked me the original question will have graduated by then. The job market will have shifted in ways neither I nor any AI can fully predict right now. The majors that looked safe in 2025 might have been hollowed out. The ones that seemed obscure might have become critical infrastructure.

In five years I'll come back and compare what the votes said to what actually happened. If this experiment is worth anything, it'll be in the delta between what people predicted and what turned out to be true.

Until then, I'm just collecting data.

---

## Update: June 2026 — What the Experiment Looks Like Now

A few weeks in. Here's what's changed.

The tool now has a proper backend. Votes used to live only in your browser's localStorage — meaning every visitor saw a different leaderboard based on their own votes. That was fine for testing, but useless as an actual experiment. I built a small PHP backend that writes every vote to a server-side JSON file with IP-based rate limiting. Now there's one shared leaderboard. When you vote, you're adding to something real.

The 757 pages are now 771. After the initial launch, I realized I needed entry points beyond the main voting page. I built 13 category and ranking pages:

- A **Top 50 Most Future-Proof** page, ranked by AI career analysis
- An **AI Picks** page — the 13 majors AI flagged specifically as high-resilience for 2025–2029
- An **AI-Resistant** page — medicine, law, and philosophy, the three categories where human presence is hardest to replace
- Category pages for all 11 academic fields: engineering, medicine, science, economics, management, law, literature, agriculture, education, history, and philosophy

Each of the 757 individual major pages now also has its own URL at `/tools/majors/[slug].html`, with roughly 1,000 words of content specific to that major's subcategory, an AI verdict, a future outlook section, and FAQ schema for search engines. That's 757 pages I never expected to write. AI helped with the structure; the differentiation logic I had to think through manually.

Current state of the experiment:

| Metric | Value |
|---|---|
| Total pages live | 771 |
| Individual major pages | 757 |
| Ranking / category pages | 13 |
| Vote backend | PHP, server-side, IP rate-limited |
| Submitted to Google | ✓ |
| Submitted to Bing/IndexNow | ✓ |
| Votes cast (as of this update) | 120 — and climbing |

The teenager who originally asked the question has finished the gaokao by now. I don't know what they chose. The tool wasn't ready in time to help them specifically — which is a strange feeling, since they were the reason I built it.

But the experiment has a five-year runway. There are more teenagers behind them.

---

*Related Reading:*
- *[I Tried to Promote My AI Experiment and Got Blocked Everywhere](/blocked-everywhere-trying-to-promote-ai-experiment/) — what happens when you build something and no one can find it*
- *[I Ran 6 AI Models on 14 World Cup Matches](/6-ai-models-predict-world-cup-china-vs-us/) — another experiment with unknown results*
- *[Free Tools →](/tools/) — including the Major Voting tool and the personal Major Advisor questionnaire*
