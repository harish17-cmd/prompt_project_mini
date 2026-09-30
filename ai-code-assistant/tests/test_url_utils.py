import unittest
from unittest.mock import patch

from app.url_utils import extract_text_from_html, fetch_url_content


class UrlUtilsTests(unittest.TestCase):
    def test_extract_text_from_html(self) -> None:
        html = """
        <html><body>
        <h1>Example Title</h1>
        <p>First paragraph.</p>
        <div><span>Second line</span></div>
        </body></html>
        """
        self.assertIn("Example Title", extract_text_from_html(html))
        self.assertIn("First paragraph.", extract_text_from_html(html))
        self.assertIn("Second line", extract_text_from_html(html))

    @patch("app.url_utils.urlopen")
    def test_fetch_url_content_reads_html(self, mock_urlopen: object) -> None:
        class FakeResponse:
            def __init__(self, body: bytes) -> None:
                self.body = body

            def read(self) -> bytes:
                return self.body

            def __enter__(self) -> "FakeResponse":
                return self

            def __exit__(self, exc_type, exc, tb) -> None:
                return None

        mock_urlopen.return_value = FakeResponse(b"<html><body><p>Hello from URL</p></body></html>")

        content = fetch_url_content("https://example.com")

        self.assertIn("Hello from URL", content)


if __name__ == "__main__":
    unittest.main()
