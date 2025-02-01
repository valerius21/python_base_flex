import unittest
from base_n import BaseN
from base_n.alphabets import BASE32_ALPHABET, BASE64_ALPHABET


class TestBaseN(unittest.TestCase):
    def setUp(self):
        """Set up test cases with common test data and encoders."""
        # Test data
        self.test_data = b"light work"
        self.empty_data = b""
        self.binary_data = bytes([0xFF, 0x00, 0xAA, 0x55])

        # Base64 setup
        self.base64_alphabet = list(BASE64_ALPHABET)
        self.base64 = BaseN(self.base64_alphabet)
        self.base64_sep = BaseN(self.base64_alphabet, separator="-")

        # Base32 setup
        self.base32_alphabet = list(BASE32_ALPHABET)
        self.base32 = BaseN(self.base32_alphabet)

        # Base16 (hex) setup
        self.base16_alphabet = list("0123456789ABCDEF=")
        self.base16 = BaseN(self.base16_alphabet)

    def test_base64_encoding(self):
        """Test Base64 encoding with various inputs."""
        # Test normal string
        encoded = self.base64.encode(self.test_data)
        self.assertEqual(encoded, "bGlnaHQgd29yaw==")

        # Test empty string
        self.assertEqual(self.base64.encode(self.empty_data), "")

        # Test binary data
        self.assertEqual(self.base64.encode(self.binary_data), "/wCqVQ==")

    def test_base64_decoding(self):
        """Test Base64 decoding with various inputs."""
        # Test normal string
        decoded = self.base64.decode("bGlnaHQgd29yaw==")
        self.assertEqual(decoded, self.test_data)

        # Test empty string
        self.assertEqual(self.base64.decode(""), b"")

        # Test binary data
        self.assertEqual(self.base64.decode("/wCqVQ=="), self.binary_data)

    def test_base64_with_separator(self):
        """Test Base64 encoding/decoding with separators."""
        # Test encoding with separator
        encoded = self.base64_sep.encode(self.test_data)
        self.assertIn("-", encoded)

        # Test decoding with separator
        decoded = self.base64_sep.decode(encoded)
        self.assertEqual(decoded, self.test_data)

    def test_base32(self):
        """Test Base32 encoding/decoding."""
        # Test normal string
        encoded = self.base32.encode(self.test_data)
        self.assertEqual(encoded, "NRUWO2DUEB3W64TL")
        self.assertEqual(self.base32.decode(encoded), self.test_data)

        # Test empty string
        self.assertEqual(self.base32.encode(self.empty_data), "")
        self.assertEqual(self.base32.decode(""), b"")

        # Test binary data
        encoded_binary = self.base32.encode(self.binary_data)
        self.assertEqual(self.base32.decode(encoded_binary), self.binary_data)

    def test_base16(self):
        """Test Base16 (hex) encoding/decoding."""
        # Test normal string
        encoded = self.base16.encode(self.test_data)
        self.assertEqual(self.base16.decode(encoded), self.test_data)

        # Test binary data
        encoded = self.base16.encode(self.binary_data)
        self.assertEqual(encoded, "FF00AA55")
        self.assertEqual(self.base16.decode(encoded), self.binary_data)

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Test padding handling
        single_byte = b"a"
        encoded = self.base64.encode(single_byte)
        self.assertIn("==", encoded[-2:])
        self.assertEqual(self.base64.decode(encoded), single_byte)

        # Test different input lengths
        for i in range(10):
            test_data = b"a" * i
            encoded = self.base64.encode(test_data)
            decoded = self.base64.decode(encoded)
            self.assertEqual(decoded, test_data)

    def test_invalid_input(self):
        """Test handling of invalid input."""
        # Test invalid alphabet (not power of 2)
        with self.assertRaises(ValueError):
            BaseN(list("ABC="))

        # Test duplicate characters in alphabet
        with self.assertRaises(ValueError):
            BaseN(list("AABCD="))

        # Test invalid character in encoded string
        with self.assertRaises(KeyError):
            self.base64.decode("Invalid!")

    def test_encode_decode_with_separator(self):
        """Test encoding and decoding with a separator."""
        encoded = self.base64_sep.encode(self.test_data)
        self.assertIn("-", encoded)
        decoded = self.base64_sep.decode(encoded)
        self.assertEqual(self.test_data, decoded)

    def test_duplicate_characters_in_alphabet(self):
        """Test that duplicate characters in alphabet raise ValueError."""
        duplicate_alphabet = list(
            "AABCDEFG="
        )  # 8 chars (power of 2) with duplicate 'A'
        with self.assertRaises(ValueError) as context:
            BaseN(duplicate_alphabet)
        self.assertEqual(
            str(context.exception), "Alphabet contains duplicate characters"
        )

    def test_empty_input(self):
        # Test empty input
        self.assertEqual(self.base64.encode(self.empty_data), "")
        self.assertEqual(self.base64.decode(""), b"")
        self.assertEqual(self.base32.encode(self.empty_data), "")
        self.assertEqual(self.base32.decode(""), b"")
        self.assertEqual(self.base16.encode(self.empty_data), "")
        self.assertEqual(self.base16.decode(""), b"")


if __name__ == "__main__":
    unittest.main()
