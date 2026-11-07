import unittest
from mcp_config_check import validate


class ConfigTests(unittest.TestCase):
    def test_root(self):
        for value in (None, [], {}, {'mcpServers': []}):
            self.assertTrue(validate(value))

    def test_valid_local(self):
        self.assertEqual(validate({'mcpServers': {'local': {'command': 'python', 'args': ['server.py']}}}), [])

    def test_valid_remote(self):
        for transport in ('http', 'streamable-http', 'sse'):
            self.assertEqual(validate({'mcpServers': {'remote': {'type': transport, 'url': 'https://example.com/mcp'}}}), [])

    def test_invalid_server(self):
        for server in (None, {'command': ''}, {'command': 'x', 'args': 'x'}, {'type': 'http', 'url': 4}, {'command': 'x', 'env': {'KEY': 4}}, {'type': []}):
            self.assertTrue(validate({'mcpServers': {'test': server}}))

    def test_no_secret_echo(self):
        self.assertNotIn('SECRET', str(validate({'mcpServers': {'SECRET': {'type': 'http', 'url': 'SECRET'}}})))


if __name__ == '__main__':
    unittest.main()
