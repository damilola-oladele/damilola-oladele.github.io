#!/usr/bin/env python3
"""
Build-time script to generate semantic embeddings for all blog posts.

Run by Netlify as part of the build command before `jekyll build`.
Reads all Markdown files in _posts/, generates a 384-dimensional embedding
for each post using bge-small-en-v1.5, and writes the results to
assets/js/data/semantic-index.json.

Usage:
    python scripts/generate_embeddings.py
"""

import json
import re
import sys
from pathlib import Path


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

    if not records:
        print("WARNING: No embeddable posts found after filtering. Nothing to write.")
        sys.exit(0)

    print(f"Embedding {len(records)} post(s) ({skipped} skipped)...")

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
