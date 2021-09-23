import os
import tarfile
from tempfile import TemporaryDirectory
from urllib import request


def generate_temp_dir() -> TemporaryDirectory:
    """
    Creates a temporary directory and returns the object.
    """
    return TemporaryDirectory()


def download_file(
    url: str, temp_dir: TemporaryDirectory, extract_file_path: str
) -> TemporaryDirectory:
    """
    Downloads the contents(tar file) from the external url and extracts the file passed as `extract_file_path` from the
    tar file.

    :param url: An external url from where the tar file needs to be downloaded.
    :param temp_dir: A temporary directory instance.
    :param extract_file_path: The path of file which has to be extracted.
    :return: temporary directory instance where the file is extracted.
    """
    file_name = str(url.split("/")[-1])
    target_path = os.path.join(temp_dir.name, file_name)
    request.urlretrieve(url, target_path)
    tar_file = tarfile.open(target_path)
    tar_file.extract(extract_file_path, temp_dir.name)
    tar_file.close()
    return temp_dir


def join_paths(prefix: str, suffix: str) -> str:
    """
    Joins the prefix and suffix as an os path.

    :param prefix: A prefix path.
    :param suffix: A suffix path/file-name.
    :return: Joined path of prefix and suffix.
    """
    return os.path.join(prefix, suffix)
