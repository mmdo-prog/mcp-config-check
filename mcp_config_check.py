"""Offline structural checks for Claude Code .mcp.json files (Python 3.9+)."""
import argparse
import json
from pathlib import Path


def validate(config):
    errors = []
    if not isinstance(config, dict) or not isinstance(config.get('mcpServers'), dict):
        return ['mcpServers must be an object.']
    for index, server in enumerate(config['mcpServers'].values(), 1):
        prefix = f'Server #{index}: '
        if not isinstance(server, dict):
            errors.append(prefix + 'configuration must be an object.')
            continue
        transport = server.get('type', 'stdio')
        if transport == 'stdio':
            if not isinstance(server.get('command'), str) or not server['command'].strip():
                errors.append(prefix + 'stdio requires a non-empty command string.')
            if 'url' in server:
                errors.append(prefix + 'url requires an explicit remote transport type.')
            args = server.get('args', [])
            if not isinstance(args, list) or any(not isinstance(a, str) for a in args):
                errors.append(prefix + 'args must be an array of strings.')
        elif isinstance(transport, str) and transport in ('http', 'streamable-http', 'sse', 'ws'):
            url = server.get('url')
            schemes = ('ws://', 'wss://') if transport == 'ws' else ('http://', 'https://')
            if not isinstance(url, str) or not (url.startswith(schemes) or url.startswith('${')):
                errors.append(prefix + 'url must use the transport scheme or an environment reference.')
        else:
            errors.append(prefix + 'unsupported transport type.')
        for field in ('env', 'headers'):
            value = server.get(field, {})
            if not isinstance(value, dict) or any(not isinstance(v, str) for v in value.values()):
                errors.append(prefix + field + ' must map names to strings.')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', default='.mcp.json')
    args = parser.parse_args()
    try:
        config = json.loads(Path(args.path).read_text(encoding='utf-8-sig'))
    except json.JSONDecodeError as exc:
        print(f'Invalid JSON at line {exc.lineno}, column {exc.colno}.')
        return 2
    except (OSError, UnicodeError):
        print('Cannot read configuration as UTF-8.')
        return 2
    errors = validate(config)
    for error in errors:
        print(error)
    if not errors:
        print('OK: supported structural checks passed.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
