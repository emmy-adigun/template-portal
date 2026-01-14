"""
imghdr module for Python 3.13+ compatibility
Streamlit requires this module which was removed in Python 3.13
"""

import os
import struct


def what(file, h=None):
    """
    Determine the type of image contained in a file or byte string.
    This is a simplified version that returns common image types.
    """
    try:
        if h is None:
            # Try to read from file
            if not os.path.exists(file):
                return None
            with open(file, 'rb') as f:
                h = f.read(32)

        if not h or len(h) < 12:
            return None

        # Check for JPEG (starts with FF D8 FF)
        if h[0] == 0xff and h[1] == 0xd8 and h[2] == 0xff:
            return 'jpeg'

        # Check for PNG
        if h.startswith(b'\x89PNG\r\n\x1a\n'):
            return 'png'

        # Check for GIF
        if h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
            return 'gif'

        # Check for BMP
        if h.startswith(b'BM'):
            return 'bmp'

        # Check for WebP (RIFF....WEBP)
        if h.startswith(b'RIFF') and len(h) >= 12 and h[8:12] == b'WEBP':
            return 'webp'

        # Check for TIFF
        if h.startswith(b'II\x2a\x00') or h.startswith(b'MM\x00\x2a'):
            return 'tiff'

        return None
    except Exception:
        return None


def test(file, h=None):
    """Alias for what() function"""
    return what(file, h)


# Define module exports
__all__ = ['what', 'test']