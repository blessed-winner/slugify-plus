# slugify-plus

`slugify-plus` is a lightweight, dependency-free Python package designed to convert human-readable text into clean, URL-friendly slugs using standard library primitives.

## Installation

Install the package in editable mode:

```bash
pip install -e .
```

## Usage

```python
from slugify_plus import slugify

slugify("My First Blog Post!")
# "my-first-blog-post"

slugify("Hello World", separator="_")
# "hello_world"

slugify("  Python   Is   Awesome  ")
# "python-is-awesome"

slugify("Build & Deploy")
# "build-deploy"
```

## Behavior

`slugify-plus` processes input strings according to predictable V1 rules:

- **Lowercase Conversion**: All letters are converted to lowercase.
- **Whitespace Normalization**: Multiple consecutive whitespace characters are collapsed into a single word boundary.
- **Punctuation Removal**: Non-alphanumeric characters and punctuation (e.g. `!`, `&`, `,`) are removed or stripped out.
- **Separator Handling**: Words are joined using the requested separator (defaults to `-`). Leading, trailing, and repeated separators are automatically removed or collapsed.
- **Unicode Normalization**: Unicode accent marks (e.g., `é`, `ñ`) are stripped using NFKD decomposition.

## Development

Install development dependencies and execute tests:

```bash
pip install -e ".[dev]"
pytest
```

## Future possibilities

Potential feature enhancements for future versions include:

- Maximum slug length truncation
- Full language transliteration (e.g., Cyrillic, Greek, Hanzi)
- Reserved-word handling (e.g., system/URL keywords)
- Uniqueness helpers (e.g., appending numeric suffixes)
- Custom normalization rules and character mapping
- Configurable character policies (e.g., preserving specific punctuation)
- Slug generation directly from database records or ORM models
