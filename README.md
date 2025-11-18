# fetch-markdown

`fetch-markdown` fetches a webpage and returns cleaned Markdown, either via a
library call or a CLI command.

Much of the extraction logic is adapted from the
[Fetch MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/fetch).

## Installation

```bash
pip install fetch-markdown
```

## Library usage

```python
from pathlib import Path
from fetch_markdown import fetch_markdown

markdown = fetch_markdown("https://huggingface.co/unsloth/GLM-4.6-GGUF")
print(markdown[:200])

output_path = Path("/tmp/model-card.md")
fetch_markdown(
    "https://huggingface.co/unsloth/GLM-4.6-GGUF",
    output_path=output_path,
)
```

## CLI usage

```bash
python -m fetch_markdown https://huggingface.co/unsloth/GLM-4.6-GGUF

# or
fetch-markdown --output output.md https://huggingface.co/unsloth/GLM-4.6-GGUF
```

## Parameters

The library function and CLI share the same core arguments/options:

- `url` (positional for CLI / first argument for library): target page.
- `output_path` / `-o/--output PATH`: optional destination file; stdout is used
  when omitted.
- `force_raw` / `--raw`: skip simplification and emit the response body verbatim.
- `user_agent` / `--user-agent STRING`: override the default identifier.
- `ignore_robots_txt` / `--ignore-robots`: skip robots.txt checks (use sparingly).
- `proxy_url` / `--proxy URL`: HTTP(S) proxy forwarded to httpx.
- `timeout` / `--timeout SECONDS`: request timeout (default 30 seconds).

## Notes

- The CLI and library both fetch live webpages; network availability and site
  rate limits apply.
- Content extraction follows the upstream MCP `fetch` server, so results mirror
  that behavior when converting pages to Markdown.
