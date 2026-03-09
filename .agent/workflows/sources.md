# /sources — Load framework sources (NOT sources-full)

## Purpose
Load *all* atomic source files from the active framework’s `sources/` directory into working context, so the AI can reference the full set of principles/content without pulling `sources-full/` verbatim dumps.

## Where the content lives
- **Primary:** `.context/specs/sources/<framework-slug>/`
- **Included:** all `*.md` files under that framework’s `sources/` folder
- **Excluded:** any `sources-full/` folders and any `*-full.md` / verbatim-only variants

## How to use it in conversation
Use this command when:
- You want the AI to “have the whole framework loaded” for navigation, referencing, linking, or synthesis
- You are about to ask questions that assume access to the *entire* sources set (principles, parts, etc.)

Do **not** use this command when:
- You explicitly need **verbatim** source text (use your sources-full workflow for that)
- You only need a single principle (load that one file directly)

## Command behavior (operational)
When `/sources` is invoked, the AI should:

1. **Identify active framework**
   - Use current session state (or ask once if unknown): `<framework-slug>`.

2. **Enumerate load targets**
   - Collect all markdown files under:
     - `.context/specs/sources/<framework-slug>/`
   - Exclude:
     - `.context/specs/sources-full/<framework-slug>/`
     - any file path containing `sources-full`
     - any file ending in `*-full.md`

3. **Load in sequence order**
   - Prefer a master outline index if present:
     - `<framework-slug>-master-outline.md` (or equivalent) → use its order.
   - Otherwise sort by:
     - numeric principle/part id (zero-padded) → then filename.

4. **Confirm loaded set**
   - Respond with:
     - Framework slug
     - Count of files loaded
     - First + last IDs loaded
     - Any missing expected IDs (if sequence gaps detected)

## Index
- Framework sources root: `.context/specs/sources/<framework-slug>/`
- If present, master outline file:
  - `.context/<framework-slug>/<framework-slug>-master-outline.md`
  - or `.context/specs/<framework-slug>-master-outline.md`
  *(use whatever exists in-repo; do not invent paths)*

## Notes
- This command loads *operational* sources only (clean, structured atoms).
- It intentionally avoids verbatim dumps to keep context efficient and reduce duplication.
