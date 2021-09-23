import os

from django.test import TestCase

from cran.libs.filestore import (
    generate_temp_dir,
    download_file,
    join_paths,
    TemporaryDirectory,
)


class FilestoreTestCase(TestCase):
    def test_generate_temp_dir(self):
        temp_dir = generate_temp_dir()
        self.assertEqual(
            type(temp_dir), TemporaryDirectory, "test_generate_temp_dir failed!"
        )

    def test_join_paths(self):
        prefix = "/root/test/"
        suffix = "file.txt"
        output = join_paths(prefix, suffix)
        expected_output = "/root/test/file.txt"
        self.assertEqual(output, expected_output, "test_join_paths failed!")

    def test_download_file(self):
        url = "https://cran.r-project.org/src/contrib/aaSEA_1.1.0.tar.gz"
        temp_dir = generate_temp_dir()
        extract_file_path = "aaSEA/DESCRIPTION"
        output = download_file(
            url=url, temp_dir=temp_dir, extract_file_path=extract_file_path
        )
        expected_path = join_paths(temp_dir.name, extract_file_path)
        self.assertEqual(
            os.path.exists(expected_path), True, "Extracted file not present."
        )
        extracted_file_path = join_paths(output.name, extract_file_path)
        self.assertEqual(
            extracted_file_path, expected_path, "test_download_file failed!"
        )
