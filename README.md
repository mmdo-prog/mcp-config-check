# MCP Config Check

A small, dependency-free, offline checker for Claude Code project `.mcp.json` files.

Requires Python 3.9+. No API key, paid service, installation or network access needed.

```sh
python mcp_config_check.py examples/valid.json
python mcp_config_check.py /path/to/.mcp.json
python -m unittest -v
```

Checks the `mcpServers` object, local command and argument types, supported remote transport URL prefixes, and string values in `env` and `headers`. A remote URL without an explicit transport is reported.

Exit codes: 0 = supported checks passed; 1 = structural issues; 2 = unreadable file or invalid JSON. Diagnostics identify servers by position and do not print configuration values, server names or JSON source lines.

## Scope

This is an independent starter tool, not an official Anthropic product or a complete schema validator. It never starts a server, resolves environment references, validates credentials or proves connectivity. Empty configurations pass. Unknown fields are retained and ignored. Environment references in remote URLs are accepted without expansion. Passing checks does not establish that a configuration is safe or that Claude Code will accept it.

Reference: https://code.claude.com/docs/en/mcp

## Contributing

Report a reproducible issue with a sanitized configuration and expected behavior. Never include real tokens or private endpoints. Add a regression test when proposing a fix. Useful next steps include stricter URL checks and optional environment-reference validation.

License: MIT. No existing adoption or Anthropic affiliation is claimed.
