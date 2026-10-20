import pytest
from slugify_plus import slugify, unique_slug


# ===========================================================================
# V1 — core slugify tests (unchanged)
# ===========================================================================

def test_basic_conversion():
    assert slugify("Hello World") == "hello-world"


def test_lowercase_conversion():
    assert slugify("MY BLOG POST") == "my-blog-post"


def test_whitespace_handling():
    assert slugify("python is awesome") == "python-is-awesome"


def test_repeated_whitespace():
    assert slugify("  Python   Is   Awesome  ") == "python-is-awesome"


def test_punctuation_removal():
    assert slugify("Hello, World!") == "hello-world"
    assert slugify("Build & Deploy") == "build-deploy"


def test_leading_trailing_whitespace():
    assert slugify("  hello world  ") == "hello-world"


def test_leading_trailing_punctuation():
    assert slugify("!!!Hello!!!") == "hello"


def test_repeated_separators():
    assert slugify("hello--world") == "hello-world"


def test_custom_separator():
    assert slugify("Hello World", separator="_") == "hello_world"
    assert slugify("Python & Java", separator=".") == "python.java"


def test_empty_string():
    assert slugify("") == ""


def test_input_only_punctuation():
    assert slugify("!@#$%^&*()") == ""


def test_input_only_whitespace():
    assert slugify("   \t\n  ") == ""


def test_invalid_text_type():
    with pytest.raises(TypeError, match="Input text must be a string"):
        slugify(123)  # type: ignore

    with pytest.raises(TypeError, match="Input text must be a string"):
        slugify(None)  # type: ignore


def test_invalid_separator_type():
    with pytest.raises(TypeError, match="Separator must be a string"):
        slugify("Hello World", separator=123)  # type: ignore


def test_empty_separator():
    with pytest.raises(ValueError, match="Separator cannot be empty"):
        slugify("Hello World", separator="")


def test_unicode_text():
    assert slugify("Café & Crème") == "cafe-creme"
    assert slugify("Pythön 3.10") == "python-3-10"
    assert slugify("El Niño") == "el-nino"


# ===========================================================================
# V2 — max_length truncation
# ===========================================================================

def test_max_length_no_truncation_needed():
    # Slug is shorter than max_length — returned unchanged
    assert slugify("Hello World", max_length=50) == "hello-world"


def test_max_length_exact_fit():
    # Slug length equals max_length exactly — returned unchanged
    slug = slugify("Hello World")        # "hello-world" (11 chars)
    assert slugify("Hello World", max_length=11) == slug


def test_max_length_word_boundary_default():
    # "my-first-blog-post" → trim at word boundary within 14 chars
    # "my-first-blog-" → boundary at index 13 → "my-first-blog"
    result = slugify("my first blog post", max_length=14)
    assert result == "my-first-blog"
    assert len(result) <= 14


def test_max_length_word_boundary_multiple_words_removed():
    result = slugify("hello world foo bar", max_length=10)
    assert result == "hello"
    assert len(result) <= 10


def test_max_length_hard_cut():
    # word_boundary=False → cut at exactly max_length characters
    result = slugify("my first blog post", max_length=10, word_boundary=False)
    assert result == "my-first-b"
    assert len(result) == 10


def test_max_length_hard_cut_strips_trailing_separator():
    # If the hard cut lands on a separator it should be stripped
    # "hello-world" cut at 6 → "hello-" → strip → "hello"
    result = slugify("hello world", max_length=6, word_boundary=False)
    assert not result.endswith("-")
    assert len(result) <= 6


def test_max_length_single_word_longer_than_limit():
    # No word boundary available — falls back to hard cut
    result = slugify("superlongword", max_length=5)
    assert result == "super"
    assert len(result) <= 5


def test_max_length_invalid_type():
    with pytest.raises(ValueError, match="max_length must be a positive integer"):
        slugify("hello", max_length=0)

    with pytest.raises(ValueError, match="max_length must be a positive integer"):
        slugify("hello", max_length=-1)


# ===========================================================================
# V2 — reserved word handling
# ===========================================================================

RESERVED = {"admin", "login", "logout", "register"}


def test_reserved_raises_on_match():
    with pytest.raises(ValueError, match="reserved word"):
        slugify("admin", reserved=RESERVED)


def test_reserved_raises_for_mixed_case_input():
    # "Admin!" normalises to "admin" which is in the reserved set
    with pytest.raises(ValueError, match="reserved word"):
        slugify("Admin!", reserved=RESERVED)


def test_reserved_allows_non_reserved_slug():
    assert slugify("my blog post", reserved=RESERVED) == "my-blog-post"


def test_reserved_empty_slug_not_checked():
    # An empty slug result should pass through without raising
    assert slugify("!!!", reserved=RESERVED) == ""


def test_reserved_invalid_type():
    with pytest.raises(TypeError, match="reserved must be a set"):
        slugify("hello", reserved=["admin"])  # type: ignore


# ===========================================================================
# V2 — unique_slug helper
# ===========================================================================

def test_unique_slug_base_not_taken():
    taken: set = set()
    result = unique_slug("my-post", exists=lambda s: s in taken)
    assert result == "my-post"


def test_unique_slug_base_taken_appends_2():
    taken = {"my-post"}
    result = unique_slug("my-post", exists=lambda s: s in taken)
    assert result == "my-post-2"


def test_unique_slug_multiple_collisions():
    taken = {"my-post", "my-post-2", "my-post-3"}
    result = unique_slug("my-post", exists=lambda s: s in taken)
    assert result == "my-post-4"


def test_unique_slug_exhausted_raises():
    # Every candidate is "taken" — should raise RuntimeError
    with pytest.raises(RuntimeError, match="unique slug"):
        unique_slug("x", exists=lambda s: True, max_attempts=5)


def test_unique_slug_invalid_base_type():
    with pytest.raises(TypeError, match="base_slug must be a string"):
        unique_slug(123, exists=lambda s: False)  # type: ignore


def test_unique_slug_invalid_exists_type():
    with pytest.raises(TypeError, match="exists must be a callable"):
        unique_slug("my-post", exists="not-callable")  # type: ignore


def test_unique_slug_invalid_max_attempts():
    with pytest.raises(ValueError, match="max_attempts must be a positive integer"):
        unique_slug("my-post", exists=lambda s: False, max_attempts=0)


def test_unique_slug_combined_with_slugify():
    # End-to-end: slugify a title then make it unique
    taken = {"my-first-blog-post", "my-first-blog-post-2"}
    base = slugify("My First Blog Post!")
    result = unique_slug(base, exists=lambda s: s in taken)
    assert result == "my-first-blog-post-3"
