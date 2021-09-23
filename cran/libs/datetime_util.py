from datetime import datetime


def string_to_datetime(datetime_str: str):
    """
    A utility method to convert datetime string into datetime object.

    :param datetime_str: A datetime string.
    :return: A datetime object of format YYYY-MM-DD HH:MM:SS.
    """
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
