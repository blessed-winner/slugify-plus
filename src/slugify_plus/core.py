import unicodedata
from typing import Callable, Optional, Set


def slugify(
    text: str,
    separator: str = "-",
    max_length: Optional[int] = None,
    word_boundary: bool = True,
    reserved: Optional[Set[str]] = None,
) -> str:
    """Convert human-readable text into a clean URL-friendly slug.

    Args:
        text: The input string to convert into a slug.
        separator: The separator string to use between words. Defaults to "-".
        max_length: Maximum number of characters in the returned slug.
                    When None (default) no truncation is applied.
        word_boundary: When True (default) and max_length is set, the slug is
                       trimmed at the last full word that fits.  When False the
                       slug is hard-cut at exactly max_length characters.
        reserved: An optional set of slug strings that are not allowed.
                  If the generated slug matches any entry a ValueError is raised.

    Returns:
        A clean, URL-friendly slug string.

    Raises:
        TypeError: If ``text`` or ``separator`` is not a string.
        TypeError: If ``reserved`` is provided but is not a set.
        ValueError: If ``separator`` is empty.
        ValueError: If ``max_length`` is provided but is not a positive integer.
        ValueError: If the generated slug matches a word in ``reserved``.
    """
    # --- Input validation ---
    if not isinstance(text, str):
        raise TypeError("Input text must be a string.")
    if not isinstance(separator, str):
        raise TypeError("Separator must be a string.")
    if not separator:
        raise ValueError("Separator cannot be empty.")
    if max_length is not None:
        if not isinstance(max_length, int) or max_length < 1:
            raise ValueError("max_length must be a positive integer.")
    if reserved is not None and not isinstance(reserved, set):
        raise TypeError("reserved must be a set of strings.")

    # --- Core slugification ---

    # Normalize unicode characters (NFKD decomposition)
    normalized = unicodedata.normalize("NFKD", text)

    # Strip accent marks (combining diacritical marks)
    stripped = "".join(c for c in normalized if unicodedata.category(c) != "Mn")

    # Lowercase and convert non-alphanumeric characters to spaces
    cleaned = "".join(c if c.isalnum() else " " for c in stripped.lower())

    # Split on whitespace runs and join with separator
    words = cleaned.split()
    slug = separator.join(words)

    # --- Max length truncation ---
    if max_length is not None and len(slug) > max_length:
        if word_boundary:
            # Trim to max_length then cut back to the last full word
            truncated = slug[:max_length]
            boundary = truncated.rfind(separator)
            if boundary > 0:
                slug = truncated[:boundary]
            else:
                # Single word longer than max_length – hard-cut is the only option
                slug = truncated
        else:
            slug = slug[:max_length]

        # Remove a trailing separator that a hard-cut may have left
        while slug.endswith(separator):
            slug = slug[: -len(separator)]

    # --- Reserved word check ---
    if reserved and slug in reserved:
        raise ValueError(
            f"Slug '{slug}' is a reserved word. "
            "Choose a different input or handle the collision with unique_slug()."
        )

    return slug


def unique_slug(
    base_slug: str,
    exists: Callable[[str], bool],
    max_attempts: int = 100,
) -> str:
    """Return a unique version of ``base_slug`` by appending an incrementing
    numeric suffix until ``exists`` returns False.

    This function is intentionally framework-agnostic.  Supply any callable
    that returns True when the candidate slug is already taken:

        # Django example
        slug = unique_slug(
            slugify("My Post"),
            exists=lambda s: Article.objects.filter(slug=s).exists(),
        )

        # Plain-Python example (checking a set)
        taken = {"my-post", "my-post-2"}
        slug = unique_slug("my-post", exists=lambda s: s in taken)

    Args:
        base_slug: The starting slug to make unique.
        exists: A callable ``(str) -> bool`` that returns True if the slug
                is already in use.
        max_attempts: Maximum number of suffix values to try before giving up.
                      Defaults to 100.

    Returns:
        A unique slug string.

    Raises:
        TypeError: If ``base_slug`` is not a string or ``exists`` is not callable.
        ValueError: If ``max_attempts`` is not a positive integer.
        RuntimeError: If a unique slug could not be found within ``max_attempts``.
    """
    if not isinstance(base_slug, str):
        raise TypeError("base_slug must be a string.")
    if not callable(exists):
        raise TypeError("exists must be a callable.")
    if not isinstance(max_attempts, int) or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer.")

    # Try the base slug first
    if not exists(base_slug):
        return base_slug

    # Append incrementing numeric suffixes: base-2, base-3, …
    for n in range(2, max_attempts + 2):
        candidate = f"{base_slug}-{n}"
        if not exists(candidate):
            return candidate

    raise RuntimeError(
        f"Could not generate a unique slug after {max_attempts} attempts. "
        "Consider a longer base or a different strategy."
    )
