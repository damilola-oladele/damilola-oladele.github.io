#!/usr/bin/env python3
"""
Build-time script to generate semantic embeddings for all blog posts.

Run by Netlify as part of the build command before `jekyll build`.
Reads all Markdown files in _posts/, generates a 384-dimensional embedding
for each post using bge-small-en-v1.5, and writes the results to
assets/js/data/semantic-index.json.

It also embeds external links curated in _tabs/portfolio.md (Tutorials and
Articles) and _tabs/other-posts.md (Other Posts), using the title and the
card's hand-written <p class="card-description"> text. Links that point
back to a post already embedded from _posts/ are skipped to avoid duplicate
entries in search results.

Usage:
    python scripts/generate_embeddings.py
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

SITE_HOST = "damilola-oladele.dev"

# _tabs pages to mine for external links, and which card-container id within
# each holds the cards to embed. Other containers in these files (e.g.
# Documentation Projects, Public Speaking) are left out of semantic search.
EXTERNAL_LINK_SOURCES = [
    {
        "file": Path("_tabs/portfolio.md"),
        "container_id": "articles",
        "tag": "tutorials-and-articles",
    },
    {
        "file": Path("_tabs/other-posts.md"),
        "container_id": "articles",
        "tag": "other-posts",
    },
]


class CardExtractor(HTMLParser):
    """
    Extracts (title, url, description) from each `<div class="card">` nested
    directly inside the `<div class="card-container" id="{container_id}">`
    with the given id. Cards in other card-container sections are ignored.
    """

    def __init__(self, container_id):
        super().__init__()
        self.container_id = container_id
        self.cards = []

        self._div_depth = 0
        self._container_depth = None
        self._card_depth = None

        self._in_title_link = False
        self._current_href = None
        self._current_title_parts = []

        self._in_description = False
        self._current_description_parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if tag == "div":
            self._div_depth += 1
            classes = (attrs.get("class") or "").split()

            if self._container_depth is None and attrs.get("id") == self.container_id:
                self._container_depth = self._div_depth
            elif (
                self._container_depth is not None
                and self._card_depth is None
                and "card" in classes
            ):
                self._card_depth = self._div_depth
                self._current_href = None
                self._current_title_parts = []
                self._current_description_parts = []

        elif tag == "a" and self._card_depth is not None and self._current_href is None:
            self._in_title_link = True
            self._current_href = attrs.get("href")

        elif tag == "p" and self._card_depth is not None:
            if "card-description" in (attrs.get("class") or "").split():
                self._in_description = True

    def handle_endtag(self, tag):
        if tag == "a":
            self._in_title_link = False
        elif tag == "p":
            self._in_description = False
        elif tag == "div":
            if self._card_depth is not None and self._div_depth == self._card_depth:
                title = " ".join("".join(self._current_title_parts).split())
                description = " ".join("".join(self._current_description_parts).split())
                if self._current_href and title:
                    self.cards.append(
                        {"title": title, "url": self._current_href, "description": description}
                    )
                self._card_depth = None

            if self._container_depth is not None and self._div_depth == self._container_depth:
                self._container_depth = None

            self._div_depth -= 1

    def handle_data(self, data):
        if self._in_title_link:
            self._current_title_parts.append(data)
        elif self._in_description:
            self._current_description_parts.append(data)


def extract_external_links(source):
    """Parse one _tabs page and return the cards found in its target container."""
    import frontmatter

    file_path = source["file"]
    if not file_path.exists():
        print(f"WARNING: {file_path} not found. Skipping its external links.")
        return []

    page = frontmatter.load(str(file_path))
    parser = CardExtractor(source["container_id"])
    parser.feed(page.content)

    return [{**card, "tag": source["tag"]} for card in parser.cards]


def is_internal_url(url):
    netloc = urlparse(url).netloc
    return netloc in ("", SITE_HOST, f"www.{SITE_HOST}")


def parse_post(post_file):
    """
    Parse a Jekyll post file using python-frontmatter.
    Returns (meta dict, body plain text) or None if the post should be skipped.
    """
    import frontmatter

    post = frontmatter.load(str(post_file))
    meta = dict(post.metadata)

    # Skip unpublished or draft posts
    if meta.get("published") is False or str(meta.get("published", "")).lower() == "false":
        return None
    if meta.get("draft") is True or str(meta.get("draft", "")).lower() == "true":
        return None

    body_text = markdown_to_plain_text(post.content)

    return meta, body_text


def markdown_to_plain_text(md):
    """
    Convert Markdown to plain text by stripping common syntax.
    Keeps the semantic content while removing formatting noise.
    """
    # Remove fenced code blocks
    md = re.sub(r"```[\s\S]*?```", "", md)
    # Remove inline code
    md = re.sub(r"`[^`]+`", "", md)
    # Remove images
    md = re.sub(r"!\[.*?\]\(.*?\)", "", md)
    # Remove links but keep link text
    md = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", md)
    # Remove ATX heading markers (keep heading text)
    md = re.sub(r"^#{1,6}\s+", "", md, flags=re.MULTILINE)
    # Remove bold/italic markers
    md = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", md)
    md = re.sub(r"_{1,3}([^_]+)_{1,3}", r"\1", md)
    # Remove blockquote markers
    md = re.sub(r"^>\s+", "", md, flags=re.MULTILINE)
    # Remove horizontal rules
    md = re.sub(r"^[-*_]{3,}\s*$", "", md, flags=re.MULTILINE)
    # Remove HTML tags
    md = re.sub(r"<[^>]+>", "", md)
    # Collapse multiple blank lines
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()


def derive_url(filename, meta):
    """
    Derive a post URL. Uses the permalink field from frontmatter if present,
    otherwise falls back to the Chirpy default: /posts/:slug/
    """
    if "permalink" in meta:
        return meta["permalink"]

    stem = Path(filename).stem
    slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
    return f"/posts/{slug}/"


def normalise_tags(tags_value):
    """
    Normalise tags to a flat string regardless of how they appear in frontmatter.

    Handles:
        tags: [python, ai]          → "python ai"
        tags:                       → "python ai"
          - python
          - ai
        tags: python                → "python"
    """
    if not tags_value:
        return ""
    if isinstance(tags_value, list):
        return " ".join(str(t) for t in tags_value)
    return str(tags_value)


def build_input_string(title, tags, body_text):
    """
    Construct the string to embed for a post.

    - Title is repeated twice to give it extra weight in the vector.
    - Tags are included so tag-based queries surface relevant posts.
    - Body is truncated to 5000 characters to stay within the model's
      effective context window (~512 tokens ≈ ~2000–4000 characters of English).
    """
    truncated_body = body_text[:5000]
    return f"{title}. {title}. {tags}. {truncated_body}".strip(". ")


def main():
    posts_dir = Path("_posts")
    output_path = Path("assets/js/data/semantic-index.json")

    if not posts_dir.exists():
        print("ERROR: _posts/ directory not found. Run this script from the project root.")
        sys.exit(1)

    # Collect both .md and .markdown files, sorted for reproducible output
    post_files = sorted(
        list(posts_dir.glob("*.md")) + list(posts_dir.glob("*.markdown"))
    )

    if not post_files:
        print("WARNING: No Markdown files found in _posts/. Nothing to embed.")
        sys.exit(0)

    # ── Imports ────────────────────────────────────────────────────────────────

    try:
        import frontmatter  # python-frontmatter
    except ImportError:
        print("ERROR: python-frontmatter is not installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("ERROR: sentence-transformers is not installed.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

    # ── Load model ─────────────────────────────────────────────────────────────

    print(f"Found {len(post_files)} file(s). Loading embedding model...")

    try:
        model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    except Exception as e:
        print(f"ERROR: Failed to load embedding model: {e}")
        sys.exit(1)

    print("Model loaded.")

    # ── Parse posts ────────────────────────────────────────────────────────────

    records = []
    input_strings = []
    skipped = 0

    for post_file in post_files:
        try:
            result = parse_post(post_file)
        except Exception as e:
            print(f"WARNING: Could not parse {post_file.name}: {e}. Skipping.")
            skipped += 1
            continue

        if result is None:
            print(f"  Skipping draft/unpublished: {post_file.name}")
            skipped += 1
            continue

        meta, body_text = result
        title = str(meta.get("title", post_file.stem))
        tags = normalise_tags(meta.get("tags", ""))
        date = str(meta.get("date", ""))
        url = derive_url(post_file.name, meta)

        input_strings.append(build_input_string(title, tags, body_text))
        records.append({"title": title, "url": url, "tags": tags, "date": date})

    # ── Parse external links ───────────────────────────────────────────────────

    internal_urls = {record["url"] for record in records}
    external_added = 0
    external_skipped = 0

    for source in EXTERNAL_LINK_SOURCES:
        try:
            links = extract_external_links(source)
        except Exception as e:
            print(f"WARNING: Could not parse external links from {source['file']}: {e}. Skipping.")
            continue

        for link in links:
            if not link["url"] or not link["title"]:
                external_skipped += 1
                continue

            if is_internal_url(link["url"]) and urlparse(link["url"]).path in internal_urls:
                # Already embedded with its full post body via _posts/ above.
                external_skipped += 1
                continue

            input_strings.append(build_input_string(link["title"], link["tag"], link["description"]))
            records.append({"title": link["title"], "url": link["url"], "tags": link["tag"], "date": ""})
            external_added += 1

    if not records:
        print("WARNING: No embeddable posts or links found after filtering. Nothing to write.")
        sys.exit(0)

    print(
        f"Embedding {len(records)} entries "
        f"({skipped} post(s) skipped, {external_added} external link(s) added, "
        f"{external_skipped} external link(s) skipped)..."
    )

    # ── Generate embeddings ────────────────────────────────────────────────────

    try:
        embeddings = model.encode(
            input_strings,
            batch_size=32,
            normalize_embeddings=True,  # Enables cosine similarity via dot product
            show_progress_bar=True,
        )
    except Exception as e:
        print(f"ERROR: Embedding generation failed: {e}")
        sys.exit(1)

    # ── Write output ───────────────────────────────────────────────────────────

    index = [
        {**record, "embedding": embedding.tolist()}
        for record, embedding in zip(records, embeddings)
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        output_path.write_text(
            json.dumps(index, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        print(f"ERROR: Failed to write {output_path}: {e}")
        sys.exit(1)

    print(f"Wrote {len(index)} entries to {output_path}")


if __name__ == "__main__":
    main()
