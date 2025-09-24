import unittest

from utils import extract_explanation

# NOTE to Ian - entirely written by Cursor


class TestExtractExplanation(unittest.TestCase):
    def test_extract_explanation_with_tags(self):
        """Test extracting explanation when tags are present"""
        text = "Here is some text <EXPLANATION>This is the explanation content</EXPLANATION> and more text"
        result = extract_explanation(text)
        self.assertEqual(result, "This is the explanation content")

    def test_extract_explanation_multiline(self):
        """Test extracting multiline explanation"""
        text = """Some text before
        <EXPLANATION>
        This is a multiline
        explanation with
        multiple lines
        </EXPLANATION>
        Some text after"""
        result = extract_explanation(text)
        expected = (
            "This is a multiline\n        explanation with\n        multiple lines"
        )
        self.assertEqual(result, expected)

    def test_extract_explanation_with_whitespace(self):
        """Test extracting explanation with leading/trailing whitespace"""
        text = "Text <EXPLANATION>  \n  Explanation with whitespace  \n  </EXPLANATION> more text"
        result = extract_explanation(text)
        self.assertEqual(result, "Explanation with whitespace")

    def test_extract_explanation_no_tags(self):
        """Test when no explanation tags are present"""
        text = "This text has no explanation tags"
        result = extract_explanation(text)
        self.assertEqual(result, "")

    def test_extract_explanation_empty_tags(self):
        """Test when explanation tags are empty"""
        text = "Text <EXPLANATION></EXPLANATION> more text"
        result = extract_explanation(text)
        self.assertEqual(result, "")

    def test_extract_explanation_multiple_tags(self):
        """Test when multiple explanation tags are present - should get first one"""
        text = "Text <EXPLANATION>First explanation</EXPLANATION> middle <EXPLANATION>Second explanation</EXPLANATION> end"
        result = extract_explanation(text)
        self.assertEqual(result, "First explanation")

    def test_extract_explanation_nested_content(self):
        """Test extracting explanation with nested content"""
        text = "Text <EXPLANATION>Explanation with <brackets> and other content</EXPLANATION> more"
        result = extract_explanation(text)
        self.assertEqual(result, "Explanation with <brackets> and other content")


if __name__ == "__main__":
    unittest.main()
