# Semantic Search Feature Implementation

## Table of contents

- [Overview](#overview)
- [Implementation options](#implementation-options)
  - [Language](#language)
  - [Embedding packages](#embedding-packages)
  - [Model selection](#model-selection)
- [System design](#system-design)
  - [Build-time pipeline](#build-time-pipeline)
  - [Runtime flow](#runtime-flow)
  - [File structure](#file-structure)
  - [Configuration changes](#configuration-changes)
- [Implementation notes](#implementation-notes)
  - [Frontmatter parsing](#frontmatter-parsing)
  - [Tag normalisation](#tag-normalisation)
  - [Draft and unpublished filtering](#draft-and-unpublished-filtering)
  - [Body truncation](#body-truncation)
  - [Input string construction](#input-string-construction)
  - [URL derivation](#url-derivation)
  - [Error handling](#error-handling)
  - [Compatibility with search-display.js](#compatibility-with-search-displayjs)
  - [Suppressing SimpleJekyllSearch interference](#suppressing-simplejekyllsearch-interference)
  - [User messaging](#user-messaging)
  - [Styling](#styling)
  - [Model preloading strategy](#model-preloading)
  - [Model caching on Netlify](#model-caching-on-netlify)
- [Design rationale](#design-rationale)
  - [Why static over server-based](#why-static-over-server-based)
  - [Why a dual-mode toggle over replacement](#why-a-dual-mode-toggle-over-replacement)
  - [Why build-time embedding over runtime](#why-build-time-embedding-over-runtime)
  - [Why bge-small-en-v15 as the model](#why-bge-small-en-v15-as-the-model)
  - [Why Python for the build script](#why-python-for-the-build-script)
  - [Why Transformers.js in the browser](#why-transformersjs-in-the-browser)

## Overview

This document describes the design and implementation of semantic search on [damilola-oladele.dev](https://damilola-oladele.dev), a personal blog built on the Jekyll Chirpy theme and hosted on Netlify.

The blog previously used Simple Jekyll Search exclusively — a lightweight keyword-matching library that searches against a pre-generated `search.json` file. This works well for exact term lookups but falls short when a reader searches by meaning rather than exact words. For example, a query like "how open source projects handle contributor fatigue" would return no results even if several posts address that topic, because none of the exact words match.

Semantic search solves this by understanding the intent and meaning behind a query. It compares the conceptual similarity between the query and each post, rather than matching character strings.

The feature was designed with two core constraints:

- **Zero running cost.** The blog is static with no backend, no database, and no paid API. The solution must stay entirely within that model.
- **No UX regression.** Simple Jekyll Search is fast and reliable. Replacing it outright would make the common case — searching for a post by title or a specific term — noticeably slower. The solution must preserve the existing experience.

To satisfy both constraints, semantic search was added as an opt-in mode alongside the existing keyword search, rather than replacing it. A toggle in the search bar lets users switch between the two modes. Keyword search remains the default.

The feature is live at [damilola-oladele.dev](https://damilola-oladele.dev).

## Implementation options

This section covers the main build decisions behind semantic search: the language for the build script, the embedding packages, and the model. Each option is weighed against the constraints of a static, zero-cost blog.

### Language

Two languages are viable for the build-time embedding script: Python and Node.js.

- **Python** is the recommended choice. The machine learning ecosystem in Python is significantly more mature than in Node.js. Libraries like `sentence-transformers` and `transformers` are better documented, more actively maintained, and have broader community support for embedding models. Python is also already a common language in the Netlify build environment, requiring no additional runtime configuration beyond specifying a version.

- **Node.js** is an alternative. Netlify already processes `package.json` for the Chirpy theme's front-end build (`rollup`, `stylelint`). A Node.js script using `@xenova/transformers` could run in that same environment without introducing a second language. However, the Node.js ML ecosystem is less mature and the `@xenova/transformers` package, while functional, has fewer resources and community examples than its Python equivalents.

The recommendation is Python for the build script and JavaScript (via Transformers.js) for the browser-side query embedding. This uses each language where it is strongest.

### Embedding packages

The following Python packages were evaluated for the build-time script:

| Package | Notes |
|||
| `sentence-transformers` | The standard library for running embedding models in Python. Well documented, supports `bge-small-en-v1.5` natively, and handles model download and caching automatically. **Recommended.** |
| `transformers` (Hugging Face) | The lower-level library that `sentence-transformers` wraps. More control but significantly more boilerplate for embedding tasks. Not necessary at this scale. |
| `fastembed` | A lighter-weight alternative focused on fast inference. Less community documentation and fewer examples than `sentence-transformers`. |

For the browser side, **Transformers.js** (`@xenova/transformers`) is the only practical option. It is the JavaScript port of Hugging Face Transformers, runs models using WebAssembly, and supports `bge-small-en-v1.5` in a quantized format suitable for browser loading.

### Model selection

The model must satisfy three requirements:

1. It must produce embeddings that can be compared using cosine similarity.
2. It must be small enough to load in a browser without causing unacceptable page weight.
3. It must be available in both a Python format (for build-time) and a Transformers.js-compatible format (for browser-time).

The following models were considered:

| Model | Size | Notes |
||||
| `BAAI/bge-small-en-v1.5` | ~24 MB (quantized) | Strong benchmark performance for its size. Well-supported in both `sentence-transformers` and Transformers.js. English-only. **Recommended.** |
| `Xenova/all-MiniLM-L6-v2` | ~23 MB (quantized) | Good quality. Widely used and extensively documented. Slightly lower benchmark scores than `bge-small-en-v1.5` on most retrieval tasks. |
| `BAAI/bge-m3` | ~570 MB | Multilingual and significantly more powerful than `bge-small-en-v1.5`, but far too large for browser use. Viable for build-time only if a browser model is chosen separately. |
| `Qwen3-Embedding` (Alibaba) | Varies by variant | Strong recent benchmarks. Smaller variants are emerging, but the Transformers.js ecosystem support is less established than for BGE models. Worth revisiting as the ecosystem matures. |

**`BAAI/bge-small-en-v1.5` is the chosen model.** It offers the best balance of quality, size, and tooling support for this specific deployment context. The blog is English-only, so the multilingual capability of larger models provides no benefit here.

A critical constraint: **the same model must be used for both build-time embedding and browser-time query embedding.** Vectors produced by different models occupy different numerical spaces and cannot be meaningfully compared. Using `bge-small-en-v1.5` for both guarantees that post vectors and query vectors are directly comparable.

## System design

The system is divided into two phases: a build-time pipeline that runs on Netlify's servers when the site is built, and a runtime flow that runs in the visitor's browser when they use search.

### Build-time pipeline

When a push is made to the repository, Netlify triggers a build. The build command in `netlify.toml` runs the embedding script before Jekyll builds the site:

```
pip install -r requirements.txt
↓
python scripts/generate_embeddings.py
↓
bundle exec jekyll build
```

The `generate_embeddings.py` script does the following:

1. Reads all `.md` and `.markdown` files in `_posts/`.
2. Skips posts where `published: false` or `draft: true` in frontmatter.
3. Parses each file's YAML frontmatter using `python-frontmatter` to extract the post title, tags, and date.
4. Derives the post URL from the filename, falling back to any explicit `permalink` set in frontmatter.
5. Strips the frontmatter from the file content, leaving only the Markdown body.
6. Converts the Markdown body to plain text by removing syntax such as headers, links, code fences, and inline code.
7. Truncates the body to 5,000 characters to stay within the model's effective context window.
8. Constructs an input string by concatenating the title (doubled for weight), tags, and truncated body.
9. Passes each input string through `bge-small-en-v1.5` using `sentence-transformers` to produce a 384-dimensional L2-normalised vector.
10. Writes the results as a JSON array to `assets/js/data/semantic-index.json`.

Each entry in `semantic-index.json` has the following shape:

```json
{
  "title": "Post title here",
  "url": "/posts/post-title-here/",
  "tags": "tag-one tag-two",
  "date": "2025-11-01",
  "embedding": [0.023, -0.041, 0.118, ...]
}
```

Tags are stored as a space-separated string rather than an array. This matches the format used by the browser-side rendering logic.

Jekyll then builds the site. Because `semantic-index.json` is written into `assets/js/data/` before `bundle exec jekyll build` runs, Jekyll picks it up as a static asset and includes it in the `_site/` output. It is served from the CDN alongside all other static assets.

### Runtime flow

The runtime flow describes what happens in the visitor's browser. It has three parts: the default keyword mode, the model preload that starts when the search bar opens, and the opt-in semantic mode.

#### Keyword mode (default)

When the search bar is focused and the user types a query, the existing Simple Jekyll Search implementation handles the lookup against `assets/js/data/search.json`. This path is unchanged.

- **Search bar preload:** As soon as the user clicks the search icon to open the search bar, `SemanticSearch.init()` is called in the background before the user has touched the toggle. The download starts immediately but nothing waits on it — the page continues responding normally. By the time the user notices the Semantic toggle and flips it, the model is likely already loaded or well into downloading.

This is triggered by a click listener on `#search-trigger`:

```javascript
document.getElementById('search-trigger')?.addEventListener('click', () => {
  SemanticSearch.init();
});
```

The `init()` guard (`if (isReady || isLoading) return`) ensures that if the toggle is flipped while the download is already in progress, the second call to `init()` exits immediately without starting a duplicate download.

- **Semantic mode (opt-in):** When the user activates the semantic mode toggle:

1. The keyword search input is hidden and replaced with the semantic search input.
2. If the search bar preload has already completed, the semantic input is immediately active. If it is still in progress, a status line below the topbar displays a loading message.
3. Once both the model and `semantic-index.json` are ready, the status line is cleared.
4. When the user types a query, a placeholder message is written into the results container immediately to prevent Simple Jekyll Search from filling it with its own "no results" message.
5. Transformers.js encodes the query string into a 384-dimensional vector using `bge-small-en-v1.5`.
6. The browser computes the cosine similarity (dot product on L2-normalised vectors) between the query vector and every post vector in the loaded index.
7. Posts are ranked by similarity score in descending order and the top 5 are displayed in `#search-results`.

The model is loaded once per page load. If the user closes and reopens the search panel without navigating away, the model does not reload. Subsequent searches on the same page are fast because the model stays in memory.

### File structure

The following files are added or modified:

```
project root
│
├── scripts/
│   └── generate_embeddings.py        new: build-time embedding script
│
├── assets/
│   └── js/
│       ├── data/
│       │   ├── search.json           existing, unchanged
│       │   └── semantic-index.json   new: generated at build time (gitignored)
│       │
│       └── semantic-search.js        new: browser-side semantic search logic
│
├── _includes/
│   └── topbar.html                   modified: semantic input, toggle, status line
│
├── _sass/
│   └── pages/
│       └── _semantic-search.scss     new: styles for input, toggle, status line
│
├── _sass/
│   └── pages/
│       └── _index.scss               modified: @forward 'semantic-search' added
│
├── netlify.toml                      modified: updated build command and env vars
└── requirements.txt                  new: Python dependencies for Netlify
```

`semantic-index.json` is added to `.gitignore`. It is a generated artefact that is different after every build and does not belong in version control. Netlify regenerates it fresh on every build.

### Configuration changes

Two files are changed to support the build-time pipeline. `netlify.toml` defines the build command and environment variables, and `requirements.txt` pins the Python dependencies.

- **`netlify.toml`:**

```toml
[build]
  command = "pip install -r requirements.txt && python scripts/generate_embeddings.py && bundle exec jekyll build"
  publish = "_site"

[build.environment]
  RUBY_VERSION = "3.3.4"
  PYTHON_VERSION = "3.11"
  HF_HOME = "/opt/build/cache/huggingface"
  SENTENCE_TRANSFORMERS_HOME = "/opt/build/cache/huggingface"
```

`bundle exec jekyll build` is used rather than bare `jekyll build` to ensure the exact Jekyll version pinned in `Gemfile.lock` is used, rather than whatever version is globally installed on the Netlify build image.

`HF_HOME` and `SENTENCE_TRANSFORMERS_HOME` point to Netlify's build cache directory so the model weights persist between builds where possible, avoiding repeated downloads.

- **`requirements.txt`:**

```
python-frontmatter==1.1.0
sentence-transformers==3.4.1
```

Both versions are pinned to ensure reproducible builds. `python-frontmatter` wraps PyYAML and handles all YAML frontmatter parsing correctly, including array tags, multiline strings, booleans, and nested values.

## Implementation notes

This section documents the specific decisions and edge cases handled during development. Each note describes a problem encountered and how it was resolved.

### Frontmatter parsing

The initial implementation used a hand-rolled parser to locate the `` delimiters and extract key-value pairs. This was replaced with `python-frontmatter`, which wraps PyYAML internally.

The hand-rolled approach had two correctness risks. First, using `text.find("", 3)` to locate the closing delimiter would match any `` in the document body, such as a Markdown horizontal rule, producing truncated or incorrect output. Second, the line-by-line key-value parser did not handle YAML arrays, meaning posts with tags like `[python, ai]` or the multiline `- tag` format would produce incorrect or empty tag values.

`python-frontmatter` handles all standard YAML types correctly and is the appropriate tool for this use case.

### Tag normalisation

Because `python-frontmatter` parses YAML correctly, tags may arrive as a Python list (`["python", "ai"]`), an inline string (`"python"`), or an inline array string (`"[python, ai]"`). A `normalise_tags()` function converts all formats to a consistent space-separated string before writing to the index.

This ensures the browser-side rendering code can always split on spaces without needing to handle multiple formats.

### Draft and unpublished filtering

Posts where `published: false` or `draft: true` in frontmatter are skipped. Without this filter, content that the author has explicitly excluded from the site would still appear in semantic search results.

### Body truncation

The body of each post is truncated to 5,000 characters before embedding. `bge-small-en-v1.5` has an effective context window of approximately 512 tokens, which corresponds to roughly 2,000–4,000 characters of English text. Content beyond that limit is silently ignored by the model. Truncating explicitly avoids the silent omission and keeps the input string at a predictable length.

### Input string construction

The input string for each post is constructed as:

```
{title}. {title}. {tags}. {body}
```

The title is repeated twice to give it additional weight in the resulting embedding vector, which improves retrieval relevance for title-matching queries. Tags are included in the embedded string so that tag-based queries surface relevant posts — previously tags were stored in the index but not embedded.

### URL derivation

The URL for each post is derived by stripping the `YYYY-MM-DD-` date prefix from the filename and applying the Chirpy permalink pattern `/posts/:slug/`. If the post frontmatter contains an explicit `permalink` field, that value is used instead, which makes the implementation resilient to future permalink configuration changes.

### Error handling

The following failure conditions are handled explicitly:

- Import errors for `python-frontmatter` and `sentence-transformers` print a clear message and exit with a non-zero code, which causes the Netlify build to fail visibly rather than silently producing an incomplete index.
- Individual post parsing errors are caught and logged as warnings. The affected post is skipped and the build continues, so a single malformed post does not abort the entire embedding run.
- Model loading failures print the exception and exit with a non-zero code.
- Embedding generation failures print the exception and exit with a non-zero code.
- File write failures print the exception and exit with a non-zero code.

### Compatibility with search-display.js

The Chirpy theme's `search-display.js` module manages the visibility of the search results wrapper and handles the cancel button. It targets `#search-input` by ID directly and listens for its `input` event to show and hide results.

To avoid breaking this existing behaviour, `#search-input` is never removed from the DOM. In semantic mode it is hidden with `display: none` and replaced visually by `#semantic-search-input`. The semantic input replicates the result-wrapper visibility logic from `search-display.js` in its own `input` event listener, since `search-display.js` will not fire for a different input element.

The cancel button handler in `topbar.html` is extended to also reset semantic state — clearing the semantic input value, unchecking the toggle, and restoring keyword mode — since `search-display.js`'s cancel handler only knows about keyword search.

### Suppressing SimpleJekyllSearch interference

Simple Jekyll Search fires synchronously on every `input` event on `#search-input`. In semantic mode, `#search-input` is hidden, but there is a timing gap: the semantic embedding is asynchronous and takes a small amount of time to complete. During this gap the results container is empty, which gives SimpleJekyllSearch an opportunity to write its "Oops! No results found." message.

This is suppressed by writing a placeholder message into `#search-results` immediately when a semantic query starts, before the embedding begins. SimpleJekyllSearch operates on `#search-input` which is hidden in semantic mode, so it does not fire. The placeholder occupies the container until the real results are ready.

Two placeholder messages are used:

- While the model is loading on first use: `"Setting up semantic search for the first time. Your results will appear shortly. Subsequent searches are faster unless browser cache is cleared."`
- While a query is being embedded after the model is ready: `"Searching by meaning, please wait…"`

### User messaging

The no-results message was updated to be actionable rather than just informational:

```
No semantic matches found for "{query}".
Try rephrasing as a concept or question, e.g. "challenges in open source documentation".
```

Semantic search works best with conceptual phrases rather than single keywords. The message guides users toward queries that are more likely to return results.

### Styling

A new file `_sass/pages/_semantic-search.scss` was added and registered in `_sass/pages/_index.scss` via `@forward 'semantic-search'`.

The key rules are:

- `#semantic-search-input` mirrors every property from the existing `#search-input` rule so the two inputs are visually identical. The Chirpy theme applies these styles by ID, so they do not automatically apply to a second input element.
- `search:has(#semantic-search-input:not([style*="display:none"]))` widens the search bar from 200px to 380px when semantic mode is active, using CSS `:has()` so no JavaScript is needed for the width change.
- `#search-mode-toggle` keeps the toggle compact. The label text is hidden on screens narrower than 1400px to save space.
- `#semantic-search-status` adds a subtle bottom border using `--search-border-color` so the status line visually belongs to the topbar.

### Model preloading

The model download is the only source of latency in semantic search. Once the model is loaded into memory, query embedding takes well under a second. The challenge is the initial ~24 MB download on first use.

**First approach was an idle preload on page load:** The approach used `requestIdleCallback` to start the model download automatically as soon as the browser became idle after page load:

```javascript
if ('requestIdleCallback' in window) {
  requestIdleCallback(() => SemanticSearch.init());
} else {
  setTimeout(() => SemanticSearch.init(), 2000);
}
```

The intent was that by the time a visitor opened the search bar and flipped the toggle, the model would already be loaded. In theory, `requestIdleCallback` defers work until the main thread is free, so the download should not compete with the page.

In practice this introduced a noticeable regression. On slower connections the ~24 MB model download competed with the page regardless of when it started, making the initial page experience sluggish for all visitors — including those who never use semantic search. The approach was removed.

**Current approach preloads on search bar open:** The model download now starts only when the user clicks the search icon to open the search bar:

```javascript
document.getElementById('search-trigger')?.addEventListener('click', () => {
  SemanticSearch.init();
});
```

This is a strong signal of intent — a user who opens the search bar is likely to interact with search. The download starts in the background immediately, and by the time the user notices the Semantic toggle and flips it, the model is often already loaded or well into downloading.

Crucially, the page load experience is completely unaffected. Visitors who never open search never trigger the download at all.

The `init()` guard (`if (isReady || isLoading) return`) ensures that if the toggle is flipped while the download is already in progress, the second `init()` call from the toggle handler exits immediately without starting a duplicate download.

The remaining tradeoff is that users on very slow connections who open search and immediately flip the toggle may still see the loading message briefly. This is acceptable — the alternative of downloading on every page load imposes a cost on all visitors, whereas the current approach only affects the subset who actively open search.

### Model caching on Netlify

`HF_HOME` and `SENTENCE_TRANSFORMERS_HOME` are set in `netlify.toml` to point to `/opt/build/cache/huggingface`. This is Netlify's build cache directory.

The `@netlify/plugin-cache` plugin was initially added to persist this directory between builds, but it requires either installation via `package.json` or via the Netlify UI. Since the project does not use `package.json` for this purpose, the plugin entry was removed from `netlify.toml`. The environment variables remain — they set the download location correctly — but the cache directory is not guaranteed to persist between builds. The model will re-download on each build until caching is configured separately.

## Design rationale

This section explains the reasoning behind the main design decisions. Each one weighs the chosen approach against the alternatives that were considered and set aside.

### Why static over server-based

The blog has no backend and no database. All content lives in flat Markdown files, and the site is compiled to static HTML at build time by Jekyll. Netlify serves these files from a CDN.

Introducing a server — even a serverless function — to handle semantic search queries would add infrastructure dependencies, latency from cold starts, and potential cost. It would also introduce a point of failure: if the function is down or slow, search breaks.

The static approach keeps the entire system simple. `semantic-index.json` is just a file on a CDN. Once it is downloaded by the browser, all search operations happen locally with no network dependency. This is more reliable and faster at query time than any server-based alternative.

### Why a dual-mode toggle over replacement

Simple Jekyll Search returns results in under 50 milliseconds for a query against a small JSON file. It is the right tool for a reader who knows what they are looking for and types a specific title, term, or phrase.

Semantic search, by contrast, requires the browser to load a ~24 MB model before it can process any query. On a fast connection this takes a few seconds; on a slow connection it could take longer. Making every visitor wait for this load — even those who just want to find a specific post by name — would be a clear UX regression with no benefit for that use case.

The toggle allows each mode to be used where it is genuinely better. Keyword search handles the common case efficiently. Semantic search is available for exploratory queries where the reader cannot articulate exactly what they want, or where the relevant posts use different vocabulary from the query. Neither mode is a fallback for the other; they are complementary.

### Why build-time embedding over runtime

Embedding a blog post is computationally expensive relative to embedding a short search query. Running the embedding model once at build time — on Netlify's build server, which has dedicated CPU and no user waiting on the result — is significantly more efficient than doing it in the browser.

If post embeddings were generated at runtime (in the browser), every visitor would need to download and run the model against all post content before searching. That would multiply both the data transfer and the computation cost by the number of visitors, for no additional benefit. The posts do not change between page loads, so their embeddings do not need to be recomputed on each visit.

Build-time embedding means each post is embedded exactly once per build. The results are stored in a static file and served from the CDN. The browser only needs to embed the user's query, which is a single short string and takes a fraction of the time.

### Why bge-small-en-v1.5 as the model

Several embedding models were considered (see the Model selection section above). `bge-small-en-v1.5` was chosen for the following reasons:

- It consistently outperforms `all-MiniLM-L6-v2` on English retrieval benchmarks at approximately the same file size.
- It is fully supported in both `sentence-transformers` (Python, for the build script) and Transformers.js (JavaScript, for the browser), which is a hard requirement for the dual-environment approach.
- At approximately 24 MB in quantized form, it is within an acceptable range for a one-time browser download that is triggered only when the user explicitly opts into semantic mode.
- The blog is English-only, so there is no benefit to a multilingual model.

Larger and more powerful models such as `bge-m3` or `Qwen3-Embedding` would produce higher-quality embeddings, but their size makes them inappropriate for browser loading. This trade-off is acceptable at the current scale of the blog. If the blog grows significantly or a more powerful model becomes available at a similar size, the model choice can be revisited without changing the overall architecture.

### Why Python for the build script

Python's machine learning ecosystem — particularly `sentence-transformers` — is the most mature and well-documented option for running embedding models outside the browser. The library handles model download, caching, batching, and encoding with a straightforward API. It has extensive documentation and community resources.

Node.js could also run embedding models via `@xenova/transformers`, and the existing `package.json` already establishes a Node.js environment on Netlify. However, using `@xenova/transformers` server-side is less common and less documented than the Python equivalent. The additional complexity is not justified when Python is available and better suited.

Using Python for the build script and JavaScript for the browser follows the principle of using each tool where it has the strongest ecosystem, rather than forcing one language to do everything.

### Why Transformers.js in the browser

The browser cannot run Python libraries. For the query embedding step to happen client-side without a server call, a JavaScript-native solution is required.

Transformers.js is the standard library for this. It is the official JavaScript port of Hugging Face Transformers, maintained by Hugging Face, and it supports `bge-small-en-v1.5` in a quantized ONNX format. The browser uses WebAssembly to run the model efficiently without requiring native binaries or plugins.

The alternatives — sending queries to a server for embedding, or using a different JS library — either reintroduce server dependencies or lack support for the chosen model.
