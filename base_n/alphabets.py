"""
Standard alphabets for common base-N encodings.

This module provides pre-defined alphabets for commonly used base-N encoding schemes.
Each alphabet string includes its padding character as the last character.

Available alphabets:
    - BASE16_ALPHABET: Standard Base16 (hex) alphabet
    - BASE32_ALPHABET: Standard Base32 alphabet (RFC 4648)
    - BASE58_ALPHABET: Bitcoin-style Base58 alphabet
    - BASE64_ALPHABET: Standard Base64 alphabet (RFC 4648)
    - BASE85_ALPHABET: ASCII85/Base85 alphabet
    - BASE256_ALPHABET: Extended ASCII alphabet
    - BASE512_ALPHABET: Extended character set
    - BASE1024_ALPHABET: Extended character set
    - BASE2048_ALPHABET: Extended character set
    - BASE4096_ALPHABET: Full extended character set with control chars
"""

# Standard encodings
BASE16_ALPHABET = "0123456789ABCDEF="
BASE32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567="
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz="
BASE64_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
BASE85_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~="

# Extended character sets
BASE256_ALPHABET = "".join(chr(i) for i in range(255)) + "="
BASE512_ALPHABET = (
    "".join(
        [chr(i) for i in range(33, 127)]  # Printable ASCII
        + [chr(i) for i in range(161, 567)]  # Extended Latin
    )
    + "="
)

BASE1024_ALPHABET = (
    "".join(
        [chr(i) for i in range(33, 127)]  # Printable ASCII
        + [chr(i) for i in range(161, 1079)]  # Extended Unicode
    )
    + "="
)

BASE2048_ALPHABET = (
    "".join(
        [chr(i) for i in range(33, 127)]  # Printable ASCII
        + [chr(i) for i in range(161, 2103)]  # Extended Unicode
    )
    + "="
)

# Full extended character set with control chars
BASE4096_ALPHABET = (
    "0123456789"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "!@#$%^&*()-_+=[{]};:',\"<>?/"
    + "".join(chr(i) for i in range(0, 66))  # Control chars and extended
    + "="
)
