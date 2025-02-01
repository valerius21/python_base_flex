"""
Base-N Encoding/Decoding Implementation

This module provides a flexible implementation for encoding and decoding data using
various base-N encodings (e.g., Base64, Base32, Base16, etc.). The implementation
supports custom alphabets and optional separators between encoded characters.
"""

from .base_n import BaseN

__version__ = "0.1.0"
__all__ = ["BaseN"]
