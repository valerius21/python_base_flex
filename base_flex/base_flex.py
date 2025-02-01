"""
Base-Flex Encoding/Decoding Implementation

This module provides a flexible implementation for encoding and decoding data using
various base-N encodings (e.g., Base64, Base32). The implementation supports custom
alphabets and optional separators between encoded characters.

Example usage:
    from base_flex import BaseN
    from base_flex.alphabets import BASE64_ALPHABET, BASE32_ALPHABET

    # Create a Base64 encoder
    base64 = BaseN(list(BASE64_ALPHABET))

    # Encode and decode data
    encoded = base64.encode(b"Hello, World!")
    decoded = base64.decode(encoded)

    # Create a Base32 encoder with separator
    base32 = BaseN(list(BASE32_ALPHABET), separator="-")
    encoded_32 = base32.encode(b"Hello, World!")
"""

import math
from typing import Dict, List

from .alphabets import BASE32_ALPHABET, BASE64_ALPHABET


class BaseN:
    """
    A flexible base-N encoder/decoder supporting custom alphabets and separators.

    This class implements encoding and decoding of binary data using any base-N encoding
    scheme, where N is determined by the size of the provided alphabet. The implementation
    handles padding automatically and supports optional separators between encoded characters.

    Attributes:
        alphabet (List[str]): List of characters used for encoding (excluding padding char)
        padding_char (str): Character used for padding
        separator (str): Optional string used to join encoded characters
        bits_per_char (int): Number of bits represented by each character in the alphabet
        block_size (int): Size of encoding blocks in characters
        reverse_alphabet (Dict[str, int]): Lookup table for decoding
    """

    def __init__(self, alphabet: List[str], separator: str = "") -> None:
        """
        Initialize a BaseN encoder/decoder with the given alphabet and separator.

        Args:
            alphabet: List of characters for encoding. The last character is used as padding.
            separator: Optional string to join encoded characters (default: "")

        Raises:
            ValueError: If alphabet length is not a power of 2
            ValueError: If alphabet contains duplicate characters
        """
        if (len(alphabet) - 1) & (len(alphabet) - 2) != 0:  # Check if power of 2
            raise ValueError("Alphabet length (excluding padding) must be a power of 2")
        if len(set(alphabet)) != len(alphabet):
            raise ValueError("Alphabet contains duplicate characters")

        self.alphabet: List[str] = alphabet[:-1]
        self.padding_char: str = alphabet[-1]
        self.separator: str = separator

        self.bits_per_char: int = int(math.log2(len(self.alphabet)))
        self.block_size: int = math.lcm(8, self.bits_per_char) // self.bits_per_char

        self.reverse_alphabet: Dict[str, int] = {
            char: idx for idx, char in enumerate(self.alphabet)
        }

    def encode(self, data: bytes) -> str:
        """
        Encode bytes to a base-N string.

        The encoding process:
        1. Converts input bytes to a binary string
        2. Splits binary string into n-bit chunks
        3. Converts each chunk to a base-N character
        4. Adds padding if necessary
        5. Joins characters with separator if specified

        Args:
            data: Bytes to encode

        Returns:
            Encoded string with appropriate padding
        """
        if not data:
            return ""

        binary = "".join(format(byte, "08b") for byte in data)

        padding_length = (
            self.bits_per_char - (len(binary) % self.bits_per_char)
        ) % self.bits_per_char
        binary += "0" * padding_length

        result = []
        for i in range(0, len(binary), self.bits_per_char):
            chunk = binary[i : i + self.bits_per_char]
            decimal = int(chunk, 2)
            result.append(self.alphabet[decimal])

        padding_count = (
            self.block_size - (len(result) % self.block_size)
        ) % self.block_size
        result.extend([self.padding_char] * padding_count)

        return self.separator.join(result)

    def decode(self, data: str) -> bytes:
        """
        Decode a base-N string to bytes.

        The decoding process:
        1. Removes separators and padding
        2. Converts each character back to its binary representation
        3. Concatenates binary strings
        4. Converts binary string back to bytes

        Args:
            data: Base-N encoded string to decode

        Returns:
            Decoded bytes

        Raises:
            KeyError: If input contains characters not in the alphabet
        """
        if not data:
            return b""

        if self.separator:
            data = data.replace(self.separator, "")
        data = data.rstrip(self.padding_char)

        binary = ""
        for char in data:
            value = self.reverse_alphabet[char]
            binary += format(value, f"0{self.bits_per_char}b")

        padding_length = len(binary) % 8
        if padding_length:
            binary = binary[:-padding_length]

        result = bytearray()
        for i in range(0, len(binary), 8):
            chunk = binary[i : i + 8]
            if chunk:
                result.append(int(chunk, 2))

        return bytes(result)


if __name__ == "__main__":
    test_data = b"light work"

    b64_alpabet_list = list(BASE64_ALPHABET)
    base64 = BaseN(b64_alpabet_list)
    base64_sep = BaseN(b64_alpabet_list, separator="-")
    b64_encoded = base64.encode(test_data)
    b64_decoded = base64.decode(b64_encoded)

    print("=== Base64 Test ===")
    print(f"Original: {test_data}")
    print(f"Encoded (no separator):  {b64_encoded}")
    b64_encoded_sep = base64_sep.encode(test_data)
    print(f"Encoded (with separator): {b64_encoded_sep}")
    print(f"Decoded:  {b64_decoded}")
    print(f"Success:  {test_data == b64_decoded}")
    print(
        f"Success (with separator): {test_data == base64_sep.decode(b64_encoded_sep)}"
    )
    print()

    b32_alphabet_list = list(BASE32_ALPHABET)
    base32 = BaseN(b32_alphabet_list)
    b32_encoded = base32.encode(test_data)
    b32_decoded = base32.decode(b32_encoded)

    print("=== Base32 Test ===")
    print(f"Original: {test_data}")
    print(f"Encoded:  {b32_encoded}")
    print(f"Decoded:  {b32_decoded}")
    print(f"Success:  {test_data == b32_decoded}")
