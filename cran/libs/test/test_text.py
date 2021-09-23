from django.test import TestCase

from cran.libs.text import remove_prefix, remove_suffix


class TextTestCase(TestCase):
    def test_remove_prefix(self):
        sample_text = "Mr. Sherlock Holmes"
        prefix = "Mr. "
        output = remove_prefix(text=sample_text, prefix=prefix)
        expected_output = "Sherlock Holmes"
        self.assertEqual(output, expected_output, "test_remove_prefix failed!")

        prefix = "Mrs. "
        output = remove_prefix(text=sample_text, prefix=prefix)
        expected_output = None
        self.assertEqual(output, expected_output, "test_remove_prefix failed!")

    def test_remove_suffix(self):
        sample_text = "Mr. Sherlock Holmes"
        suffix = "Holmes"
        output = remove_suffix(text=sample_text, suffix=suffix).strip()
        expected_output = "Mr. Sherlock"
        self.assertEqual(output, expected_output, "test_remove_suffix failed!")

        suffix = "Watson"
        output = remove_suffix(text=sample_text, suffix=suffix)
        expected_output = "Mr. Sherlock Holmes"
        self.assertEqual(output, expected_output, "test_remove_suffix failed!")
