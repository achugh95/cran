from django.test import TestCase

from cran.package.management.commands.populate_package import Command


class CommandTestCase(TestCase):
    def test_get_package_name(self):
        output = Command.get_package_name(item="Package: Test Package")
        expected_output = "Test Package"
        self.assertEqual(output, expected_output, "test_get_package_name failed!")

    def test_get_package_version(self):
        output = Command.get_package_version(item="Version: 1.0.1")
        expected_output = "1.0.1"
        self.assertEqual(output, expected_output, "test_get_package_version failed!")

    def test_get_publication_timestamp(self):
        output = Command.get_publication_timestamp(
            item="Date/Publication: 2021-09-23 19:00:05 UTC \n"
        )
        expected_output = "2021-09-23 19:00:05"
        self.assertEqual(
            output, expected_output, "test_get_publication_timestamp failed!"
        )

    def test_get_package_title(self):
        output = Command.get_package_title(item="Title: Package title")
        expected_output = "Package title"
        self.assertEqual(output, expected_output, "test_get_package_title failed!")

    def test_get_package_description(self):
        output = Command.get_package_description(
            item="Description: Package description"
        )
        expected_output = "Package description"
        self.assertEqual(
            output, expected_output, "test_get_package_description failed!"
        )

    def test_get_package_author(self):
        output = Command.get_package_author(
            item="Author: Anshul Chugh <achugh95@gmail.com>,Thomas Shelby <thomas!>"
        )
        expected_output = ("Anshul Chugh, Thomas Shelby", "achugh95@gmail.com")
        self.assertEqual(output, expected_output, "test_get_package_author failed!")

    def test_get_package_maintainer(self):
        output = Command.get_package_maintainer(
            item="Maintainer: Anshul Chugh <achugh95@gmail.com>"
        )
        expected_output = ("Anshul Chugh", "achugh95@gmail.com")
        self.assertEqual(output, expected_output, "test_get_package_maintainer failed!")

    def test_separate_name_and_email(self):
        output = Command.separate_name_and_email(
            person_info="Anshul Chugh <achugh95@gmail.com>"
        )
        expected_output = ("Anshul Chugh", "achugh95@gmail.com")
        self.assertEqual(
            output, expected_output, "test_separate_name_and_email failed!"
        )

    def test_validate_email(self):
        output = Command.validate_email(input_email="achugh95@gmail.com")
        self.assertEqual(output, True, "test_validate_email failed!")

        output = Command.validate_email(input_email="achugh95@gmailcom")
        self.assertEqual(output, False, "test_validate_email failed!")
