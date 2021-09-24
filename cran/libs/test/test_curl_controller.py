import json

from django.test import TestCase

from cran.libs.curl_controller import CurlController


class CurlTestCase(TestCase):
    def test_send_get_request(self):
        output = json.loads(
            CurlController.send_get_request(url="https://catfact.ninja/fact")
        )
        expected_output = {"fact": False, "length": False}
        for key, value in output.items():
            expected_output[key] = True

        for key, value in expected_output.items():
            self.assertEqual(value, True, "test_send_get_request failed!")
