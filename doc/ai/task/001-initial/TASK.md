# Task: Create the `fetch-markdown` project based on the `fetch` MCP server

Create a new Python project called **`fetch-markdown`** in an empty git repository.  
The goal is to reuse and adapt code from the existing **`fetch`** MCP server to build a small tool/library that fetches a web page and outputs **cleaned Markdown** (to stdout by default, optionally to a file).

The new project is a normal Python project (not an MCP server).

---

## Existing code to reuse

The repository will contain a git submodule with the original `fetch` project:

- Submodule checkout root (do not modify submodule contents directly):  
  `tmp_submodules/servers/`

- Inside that submodule, the Python code for the `fetch` MCP server is at:  
  `tmp_submodules/servers/src/fetch/src/mcp_server_fetch`

Assume this path exists and is readable from the `fetch-markdown` project.  
Treat the submodule as **read-only**: copy code into the new project rather than importing directly from it at runtime.

The `fetch` project is MIT licensed. When copying code, preserve license headers and any required attribution.

### Existing GitHub pipeline s template

Add a pipeline similar to /mnt/data/development/PRIVATE/github/Wuodan/llm-aggregator/.github/workflows/ci.yml.
Ensure your build system is similar to the one in `llm-aggregator`.

### Other existing files as templates

- /mnt/data/development/PRIVATE/github/Wuodan/llm-aggregator/pyproject.toml
- /mnt/data/development/PRIVATE/github/Wuodan/llm-aggregator/requirements.txt
- /mnt/data/development/PRIVATE/github/Wuodan/llm-aggregator/requirements-dev.txt

---

## Overall goal

Build a small, focused project that:

1. Reuses the extraction/cleaning logic from `mcp_server_fetch` to turn HTML pages into good Markdown.
2. Exposes this functionality:
   - As a **library function** that can be imported and called from Python.
   - As a **CLI** that reads a URL and prints Markdown to stdout by default, with an option to write to a file.
3. Includes tests (with `pytest`) that exercise the real Hugging Face site at least once and print the paths of any Markdown files they create.

The project should follow sensible Python packaging and layout practices, but the exact structure is up to you.

---

## Scope and behavior

### Supported use cases (initial version)

Focus on the following primary use case:

- Given a Hugging Face model page URL, fetch the page and produce cleaned Markdown suitable for later use as LLM context.

Example URL to target in tests and examples:

- `https://huggingface.co/unsloth/GLM-4.6-GGUF`

The tool should also work reasonably for other arbitrary web pages (within the limitations of the reused `fetch` logic), but the main acceptance target is Hugging Face model pages.

### Library API

Provide at least one public function with a clear, documented signature. For example:

```python
from pathlib import Path
from typing import Optional

def fetch_markdown(
    url: str,
    output_path: Optional[Path] = None,
) -> str:
    """Fetch the given URL and return cleaned Markdown.

    If ``output_path`` is provided, write the Markdown to that file and
    return the Markdown string.
    """
```

Requirements:

- Use/adapt the logic from `mcp_server_fetch` to:
  - Fetch the page (HTTP).
  - Extract the relevant HTML content.
  - Convert it into Markdown.
  - Apply any necessary cleaning/normalization.
- If `output_path` is `None`:
  - Do not write a file, only return the Markdown string.
- If `output_path` is not `None`:
  - Ensure the parent directory exists (create it if necessary).
  - Write the Markdown to `output_path` using UTF-8 encoding.
  - Return the Markdown string.

You may add additional helper functions or classes if that improves clarity.

### CLI behavior

Provide a small command-line interface entry point (e.g. via `python -m fetch_markdown` or a console script) with the same fetching and summarizing behavior as the MCP server `fetch`.


---

## Reusing `fetch` code

When adapting `mcp_server_fetch`:

- Identify and copy the parts responsible for:
  - Fetching HTTP content.
  - Selecting the meaningful content segment(s) from a page.
  - Converting HTML to Markdown.
  - Performing cleaning / post-processing.
- Remove or refactor away:
  - MCP-specific server wiring.
  - Protocol handling that is only relevant to MCP.
  - Any code that manages multi-client, multi-request server behavior.

You may keep the internal structure similar if it helps, but the end result should be a clean, non-MCP Python module suitable for library and CLI use.

Preserve license notices from the original files where appropriate.

---

## Dependencies and packaging

- Use Python 3.x (choose a reasonable modern version).
- Use the dependencies from `fetch`
- Configure the project in a standard way (e.g. with `pyproject.toml` and a `src/` layout), but do not over-engineer it.

Document non-standard dependencies in a way that makes it obvious how to install them (e.g. a short section in a README or comments).

---

## Python venv, Linting and PyTest

- Use only the existing venv in `.venv` to run Python code.
- Run `` to lint the code.
- Use `pytest --cov=llm_aggregator --cov-report=term-missing` to run tests. Ensure a reasonly high coverage percentage is reached. And especially test key parts of the code.


---

## Tests

Use `pytest`.

Create tests that:

1. Exercise the core library function (`fetch_markdown` or equivalent) using a **real Hugging Face page**, specifically:
   - `https://huggingface.co/unsloth/GLM-4.6-GGUF`
2. Use a temporary directory (`tmp_path`) to write Markdown output to a file.
3. Assert at minimum:
   - The file exists.
   - The file is non-empty.
4. **Print** the output file path(s) so it is easy to inspect the generated Markdown when running tests manually.

Handle network errors gracefully in tests (e.g. mark the test xfail or skip if Hugging Face is unreachable), to avoid permanent red test runs from transient network issues.

You may add additional tests (e.g. for other URLs or error paths) as appropriate.

---

## Project layout and response format

You may choose a clean project layout such as:

- `src/fetch_markdown/` for the main package.
- `tests/` for tests.
- A `pyproject.toml` or equivalent configuration file.
- Optionally a `README.md` explaining usage.
- 

Keep names and structure consistent and clean, following standard Python project practices.
