from datetime import datetime

from django.test import TestCase

from cran.libs.datetime_util import string_to_datetime


class DateTimeUtilTestCase(TestCase):
    def test_string_to_datetime(self):
        sample_datetime = "2019-11-09 16:20:02"
        output = string_to_datetime(datetime_str=sample_datetime)
        expected_output = datetime(
            year=2019, month=11, day=9, hour=16, minute=20, second=2
        )
        self.assertEqual(output, expected_output, "test_string_to_datetime failed!")
