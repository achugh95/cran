def remove_prefix(text: str, prefix: str) -> str:
    """
    A utility function to remove a prefix from a string. If the prefix does not exist, it does not return anything.

    :text: The text from which prefix needs to be removed.
    :prefix: The value of string which should be removed.
    :return: Updated text or nothing.
    """
    if text.startswith(prefix):
        return text[len(prefix) :]


def remove_suffix(text: str, suffix: str) -> str:
    """
    A utility function to remove a suffix from a string. If the suffix does not exist, it returns original text.

    :text: The text from which suffix needs to be removed.
    :suffix: The value of string which should be removed.
    :return: Updated text or original text.
    """
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text
