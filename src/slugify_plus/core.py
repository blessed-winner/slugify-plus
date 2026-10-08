import unicodedata


def slugify(text: str, separator: str = "-") -> str:
    """Convert human-readable text into a clean URL-friendly slug.

    Args:
        text: The input string to convert into a slug.
        separator: The separator string to use between words. Defaults to "-".

    Returns:
        A clean, URL-friendly slug string.

    Raises:
        TypeError: If `text` or `separator` is not a string.
        ValueError: If `separator` is empty.
    """
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if not isinstance(separator, str):
        raise TypeError("Separator must be a string.")
    if not separator:
        raise ValueError("Separator cannot be empty.")

    # Normalize unicode characters (NFKD decomposition)
    normalized = unicodedata.normalize("NFKD", text)

    # Strip accent marks (combining diacritical marks)
    stripped = "".join(c for c in normalized if unicodedata.category(c) != "Mn")

    # Lowercase and convert non-alphanumeric characters to spaces
    cleaned = "".join(c if c.isalnum() else " " for c in stripped.lower())

    # Split on whitespace runs and join with separator
    words = cleaned.split()
    return separator.join(words)
