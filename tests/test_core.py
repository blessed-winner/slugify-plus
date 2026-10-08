import pytest
from slugify_plus import slugify


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
