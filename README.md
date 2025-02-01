# Base-N Encoder/Decoder

A flexible Python implementation for encoding and decoding data using various base-N encodings (e.g., Base64, Base32, Base16, Base4096, etc.). The implementation supports custom alphabets and optional separators between encoded characters.

> **Note:** If you are looking for a faster, more robust implementation for standart encodings, use the [standard library](https://docs.python.org/3/library/base64.html).
> This library goal is to provide a flexible implementation for custom base-N encodings and alphabets!

## Features

- Support for any base-N encoding with power-of-2 alphabet size
- Built-in support for common encodings (Base64, Base32)
- Pre-defined standard alphabets in `alphabets` module
- Configurable padding character
- Optional separators between encoded characters
- Comprehensive test suite
- Type hints and detailed documentation
- Efficient implementation using bitwise operations

## Installation

```bash
pip install base-n
```

## Usage

```python
from base_n import BaseN
from base_n.alphabets import BASE64_ALPHABET, BASE32_ALPHABET

# Base64 encoding/decoding
base64 = BaseN(list(BASE64_ALPHABET))

# Basic encoding/decoding
encoded = base64.encode(b"Hello, World!")
decoded = base64.decode(encoded)

# Using separators for better readability
base64_sep = BaseN(list(BASE64_ALPHABET), separator="-")
encoded_with_sep = base64_sep.encode(b"Hello, World!")
decoded_with_sep = base64_sep.decode(encoded_with_sep)

# Base32 encoding/decoding
base32 = BaseN(list(BASE32_ALPHABET))
encoded_base32 = base32.encode(b"Hello, World!")
decoded_base32 = base32.decode(encoded_base32)

# Custom base-N encoding
# You can create your own base-N encoding by providing a custom alphabet
# The alphabet length (excluding padding char) must be a power of 2
# The last character of the alphabet is the padding character, and every element must be unique!
custom_alphabet = list("01234567=")  # Base8 example
base8 = BaseN(custom_alphabet)
encoded_base8 = base8.encode(b"Hello")
decoded_base8 = base8.decode(encoded_base8)
```

## Project Structure

```
base_n/
├── base_n/
│   ├── __init__.py
│   ├── base_n.py      # Main implementation
│   ├── alphabets.py   # Pre-defined standard alphabets
│   └── tests/
│       ├── __init__.py
│       └── test_base_n.py
├── README.md
└── pyproject.toml
```

## Running Tests

The project includes a comprehensive test suite. To run the tests:

```bash
python -m unittest discover -v && coverage report
```

## Implementation Details

The implementation follows these steps:

### Encoding

1. Converts input bytes to a binary string
2. Splits the binary string into n-bit chunks
3. Converts each chunk to a base-N character
4. Adds padding if necessary
5. Joins characters with separator (if specified)

### Decoding

1. Removes separators and padding
2. Converts each character back to its binary representation
3. Concatenates binary strings
4. Converts binary string back to bytes

### Validation

- Ensures alphabet length (excluding padding) is a power of 2
- Checks for duplicate characters in the alphabet
- Validates input characters during decoding

## License

MIT License
