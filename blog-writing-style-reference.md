# Blog Writing Style Reference

A single reference for every rule, convention, and preference that shapes writing for this blog. Sourced from the project's `writing-style-guide-blog.md` (explicit, stated rules) and cross-referenced against published posts in the project (used to confirm patterns or flag where practice diverges from the written guide).

Anything not drawn from an explicit rule in the style guide is labeled **[Inferred]** and comes from patterns observed across multiple published posts rather than a stated instruction.

---

## Voice and Tone

**Explicit rules (from the style guide):**

- Write in **second person** ("you") to address readers directly.
- Use **first-person singular** ("I," "my") when:
  - Referencing your own posts or previous work ("In my last post, I explained...")
  - Sharing personal experience ("In my experience, I often need...")
  - Making observations ("I've noticed that...")
  - Discussing what you will cover ("I will discuss in this post")
- Use **first-person plural** ("we," "our") when referring to shared professional experiences or collective practices in the field.
- Use **third person** sparingly, mainly when discussing others' work or external references.
- Write with **conviction**: make clear claims without hedging words like "likely" or "maybe."
- Maintain a **professional, instructive tone** that supports comprehension.
- Use **contractions sparingly** (e.g., "it's" instead of "it is") when natural.
- **Avoid excessive conversational transitions** — prefer direct statements.
- Acceptable: ending sentences with prepositions when natural, beginning sentences with "or," "and," or "but," using sentence fragments occasionally for emphasis.
- **Exclamation points**: use rarely, only when absolutely necessary.
- **Persuasive language**: use instructive language instead.
- **Hedging language**: write with confidence (avoid "likely," "maybe," "probably").
- Write at approximately **middle school reading level** for accessibility.

**[Inferred]** From published posts (e.g., the open-source/short-term-contracts post, the editing-matters post): personal-experience posts (like the Outreachy series) lean more heavily first-person and narrative, while instructional/explainer posts (like the smart contracts or user research posts) lean second-person and instructional. The voice shifts based on post type even though both stay within the style guide's rules.

---

## Audience

**Explicit rules:**

- **Assume readers have professional experience** in technology or technical writing.
- Don't over-explain fundamental concepts familiar to the target audience.
- Avoid jargon unless necessary for technical accuracy; when technical terms are necessary, use them correctly and consistently.
- Include relevant context but avoid over-explaining basics to the target audience.

**[Inferred]** Posts define specialized/niche terms on first use even for a technical audience (e.g., "yapping," "StreamField," "gap analysis," DPGs), suggesting the technical-audience assumption applies to general tech/writing concepts, not to niche or project-specific terminology, which still gets a plain-language definition the first time it appears.

---

## Structure and Formatting

**Explicit rules:**

- **Minimum 1,000 words** per article.
- Use the **BLUF principle** (Bottom Line Up Front): state the most important information at the beginning.
- Start general, then move to details, conditions, exceptions, and secondary information.
- Divide content into short, logical sections with clear headings.
- **H2 headings**: broad topic sections. **H3 headings**: specific sub-topics.
- Use **statement headings** that tell readers what to expect; consider **question headings** for common audience questions.
- Use **sentence case** for all headings (not title case).
- **Keep sentences short**: normally no more than two lines.
- **One idea per sentence**: break complex thoughts into multiple sentences.
- Start sentences with the main idea, not exceptions or conditions; put long conditions after the main clause.
- Keep subject, verb, and object physically close together.
- Use lots of periods — short sentences improve readability.
- **Vary paragraph length**: 1–7 sentences depending on complexity.
  - Single-sentence paragraphs: transitions, emphasis, section setup.
  - Multi-sentence paragraphs (2–7 sentences): complex ideas, detailed explanations, supporting examples.
- **One idea or topic per paragraph.**
- Use transition words/phrases to connect paragraphs smoothly.
- **Introductions**: open with a clear problem statement or resonant observation; establish why the topic matters early; set expectations for what readers will learn; use concrete examples early.
- **Body content**: support claims with specific examples from professional practice; use bold sparingly for key terms; break up long sections with subheadings.
- **Conclusions**: no separate "Conclusion" heading — content flows naturally to its end; final paragraphs synthesize key points or give next steps; use `<br><br>` spacing before the closing paragraph instead of a heading; avoid introducing new concepts in the close.
- Include a "Further reading and references" section when appropriate, formatted as an HTML unordered list of links.

**Note on quality-checklist conflict:** the style guide's Quality Checklist says "paragraphs limited to 3 sentences maximum," which conflicts with the earlier stated 1–7 sentence range. Published posts follow the 1–7 sentence range in practice (several paragraphs run 4–6 sentences), so treat the checklist's "3 sentences" line as the stricter/older rule and the "1–7 sentences" guidance as the one actually followed.

**[Inferred]** Diagrams (Mermaid) are used in at least one how-to post to visualize a process/stage flow — worth using when a process has sequential steps, though this isn't a stated rule.

---

## Grammar and Mechanics

**Explicit rules:**

- Use the **Oxford comma** consistently.
- Never end sentences/lists with "etc." — use "and" before the last item, or precede the list with "including."
- Write out numbers **one through nine**; use numerals for **10 and above**.
- Always use numerals with units of measurement or percentages.
- Use commas in numbers over 999 (e.g., 1,000).
- Companies are **things, not persons**: use "that," not "who."
- Use "from...to..." constructions only when the endpoints are extremely different.
- When using numbers, specify what they measure.
- Don't leave ambiguity when referencing concepts — fill in the blank clearly.
- **Avoid abbreviations** when possible (write "vegetables," not "veggies").
- When using standard abbreviations, **define on first use**: "call to action (CTA)"; no need to redefine more than once per article; pluralize the abbreviation if the definition is plural ("calls to action (CTAs)").
- **Em dashes**: limit to 2–3 per article; use commas or periods instead in most cases. Avoid dashes in every sentence.
- Italicize terms when introducing new concepts or emphasizing specific phrases.
- Use inline code formatting for tool names, commands, or technical terms when appropriate.

---

## Titles and Metadata

**Explicit rules (front matter format):**

```yaml
---
title: "Article title in sentence case"
description: Brief description of the article's main topic.
date: YYYY-MM-DD HH:MM:SS +0100
categories: [Documentation]
tags: [documentation]
pin: false
image:
  path: /assets/img/cover-images/filename.png
  alt: Brief description of cover image.
published: true
---
```

- **Titles use sentence case** — only the first word and proper nouns are capitalized.
- Description field: a brief, direct description of the article's main topic (not a teaser or clickbait line).

**[Inferred]** From published front matter:
- `categories` is typically a single broad category matching the blog's section (e.g., `[Documentation]`, `[Blockchain]`, `[Open Source, Outreachy]`).
- `tags` are lowercase, short, and topic-based (e.g., `[documentation, career, open-source]`).
- Cover image filenames mirror the post's slug/title.
- Series posts (like the Outreachy weekly series) keep a consistent cover image across the whole series rather than a unique one per post.
- `pin: false` and `published: true` appear to be the default state unless a post is intentionally unpublished (two crypto posts in the project are `published: false`, apparently held back).

---

## Content Conventions

**Explicit rules:**

- **Links**: use **HTML anchor tags** with `target="_blank"` for external links; provide descriptive link text indicating destination or topic.
- Reference lists: format as HTML unordered lists with links, under a "Further reading and references" heading.
- Support claims with specific examples from professional practice.
- Reference credible sources and link to external resources when appropriate.
- Use proper names for tools, frameworks, and technologies (e.g., "MkDocs," "Docusaurus").
- Use bold sparingly, for key terms/concepts only.

**[Inferred]** From published posts:
- Internal cross-references to earlier posts use relative markdown links or anchor tags pointing to `/posts/...` paths, and typically frame the reference conversationally ("In my last post, I explained...", "Last week, I shared...").
- Code samples are presented in fenced code blocks with a language identifier (` ```sh `, ` ```python `), and commands are explained in the surrounding prose before or after the block.
- Callouts/asides (caveats, tips, definitions) use Chirpy-style blockquote prompts, e.g. `> text` with `{: .prompt-info }` or `{: .prompt-tip }`.
- Mermaid diagrams are used for process flows when the content benefits from a visual (`mermaid: true` in front matter).
- GIFs/images are given descriptive alt text.

---

## Things to Avoid

**Explicit rules — Completely prohibited terms:**

- **Foster** → use "create," "build," "encourage," or "support."
- **Revolutionize** → use "transform" (except in narrative contexts).
- **Landscape** (e.g., "the fast-paced tech landscape") → rewrite without this framing.
- **"This is where X comes in"** → state directly what X does or provides.
- **"X is not just about Y; it's about Z"** → state what X is about directly.
- **"X isn't just nice to have; it's..."** → state X's importance directly.
- **"You're not alone"** → address the reader's situation directly.
- **Groundbreaking** → use "innovative," "new," or "significant."
- **Thrive in a fast-paced environment** → describe actual capabilities or results.

**Strictly limited (2–3 uses max per article):**

- **Ensure** → prefer "make sure," "guarantee," or "verify."
- **Significant/significantly** → prefer "important," "substantial," "considerable."
- **Effective/effectively** → prefer "successful," "works well," "produces results."
- **Essential** → prefer "necessary," "critical," "important."
- **Em dashes** → limit to 2–3 per article.

**Heavily restricted (minimize):**

- **Seamless** → "smooth," "integrated," or describe the actual experience.
- **Enhance** → limit to 2 per article; use "improve," "strengthen," "refine."
- **Robust** → "strong," "reliable," "powerful," or be specific.
- **Comprehensive** → "complete," "thorough," "detailed," or omit.
- **Streamline** → "simplify," "improve," "optimize."
- **Elevate** → "improve," "raise," "enhance quality."
- **Facilitate** → "enable," "support," "make possible."

**Ambiguous/unnatural terms to avoid:**

- **Dives deep** → "examines closely," "explores thoroughly," "analyzes in detail."
- **Underscoring** → "highlighting," "emphasizing," "showing."
- **Delve** → "explore," "examine," "investigate."
- **Realm** → "area," "field," "domain," or be specific.
- **Evolve** → "develop," "change," "grow" (contextually).
- **Emergence** → "appearance," "development," "rise."

**Prohibited punctuation patterns:**

- Avoid dashes in every sentence; prefer commas, periods, or semicolons for most sentence structures.

**Clichés — replace with direct alternatives:**

- "word to the wise" → "here's what you need to know"
- "can of worms" → "problem"
- "day in, day out" → "every day"
- "get your feet wet" → "try"
- "I beg to differ" → "I disagree"
- "like clockwork" → "a habit"
- "needless to say" → "that said"
- "plain as day" → "clear"
- "scared to death" → "terrified"
- "time is of the essence" → "there's a looming deadline"
- "wet behind the ears" → "inexperienced"

**Other explicit avoidances:**

- Avoid the obvious — cut information that doesn't add value.
- Avoid clichés generally — find fresh phrasing.
- Never repeat information across sections; avoid circular reasoning.
- Cut redundant modifiers/phrases: "advance planning" → "planning," "end result" → "result," "basic fundamentals" → "fundamentals"/"basics," "brief summary" → "summary," "past experience" → "experience," "completely eliminate" → "eliminate," "final outcome" → "outcome," "general consensus" → "consensus."
- Don't repeat the same words too closely together in sentences or paragraphs.
- Avoid logical jumps — provide context before introducing a new concept.
- No separate "Conclusion" heading.
- No hedging language.

---

## Examples

**From the style guide's own "Voice Examples" section (explicit):**

Preferred style:
- "Technical writers should adopt the same philosophy for documentation. Simplicity should be the cornerstone of their approach."
- "Documentation isn't just about what you think users need. It's about what they actually need."
- "The problem is simple: most technical writers create documentation based on assumptions."

Avoid:
- "It's likely that technical writers could potentially benefit from adopting a similar philosophical approach." (hedging)
- "Documentation is, for the most part, generally speaking, about meeting user needs." (hedging/filler)
- "There seems to be a problem where technical writers might create documentation based on assumptions." (hedging)

**[Inferred] Illustrative patterns pulled from published posts (not stated as rules, but consistent with the guide):**

- BLUF opening, e.g., "Short-term contracts are common in technical writing, but they come with a reputation problem." — states the topic and tension in the first sentence.
- Direct problem-statement openings, e.g., "Most people agree that collaboration is a major factor in determining the success of a documentation project. But I've noticed that they rarely define what this means in practice."
- Closing paragraphs use `<br><br>` before a final synthesizing paragraph rather than a "Conclusion" header, e.g., in the open-source/short-term-contracts post and the shared-responsibility post.
- Definitions of niche terms are set off with a blockquote immediately after first use, e.g., defining "Admin interface" or "gap analysis" inline within a `>` blockquote.

---

## Attribution

Per the style guide's own attribution note: *"This style guide synthesizes principles from The Blogsmith Style Guide with established patterns from published blog posts about technical writing and documentation. When conflicts arise, the patterns demonstrated in published work take precedence over generic style guide recommendations."*

This reference document follows that same precedence: where the style guide and observed post patterns conflict (e.g., the paragraph-length checklist item), the pattern from published work is noted as the operative one.
