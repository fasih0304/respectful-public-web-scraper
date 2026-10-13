import unittest
from scraper import parse_html, validate_url


class ParserTests(unittest.TestCase):
    def test_extracts_title_text_and_links(self):
        html = """<html><head><title>Example Page</title><script>hidden()</script></head>
        <body><h1>Hello world</h1><a href="/about">About</a></body></html>"""
        result = parse_html(html, "https://example.com/home")
        self.assertEqual(result["title"], "Example Page")
        self.assertIn("Hello world", result["text"])
        self.assertNotIn("hidden()", result["text"])
        self.assertEqual(result["links"][0]["url"], "https://example.com/about")

    def test_rejects_invalid_url(self):
        with self.assertRaises(ValueError):
            validate_url("example.com")


if __name__ == "__main__":
    unittest.main()
