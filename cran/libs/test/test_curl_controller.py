import json

from django.test import TestCase

from cran.libs.curl_controller import CurlController


class CurlTestCase(TestCase):
    def test_send_get_request(self):
        output = json.loads(
            CurlController.send_get_request(url="https://catfact.ninja/fact")
        )
        output_keys = list(output.keys())
        expected_output_keys = ["fact", "length"]
        self.assertEqual(
            output_keys, expected_output_keys, "test_send_get_request failed!"
        )
