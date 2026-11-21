# SPDX-License-Identifier: MIT
"""TM1680 I2C driver for 16x16 monochrome panels wired like CoreMatrix."""

import errno
import framebuf


class TM1680(framebuf.FrameBuffer):
    """Draw with framebuf methods, then send the pixels with show()."""

    def __init__(self, i2c, address=0x72, brightness=2):
        self._check_brightness(brightness)
        self._i2c = i2c
        self._address = address
        self._pixels = bytearray(32)
        self._packet = bytearray(33)  # First byte addresses display RAM at 0.
        super().__init__(self._pixels, 16, 16, framebuf.MONO_HMSB)
        # Display off, oscillator off, 24 ROW x 16 COM (NMOS), RC master, oscillator on.
        self._write(b"\x82\x80\xa4\x98\x81")
        self.show()
        self.brightness(brightness)

    def _write(self, data):
        if self._i2c.writeto(self._address, data) != len(data):
            raise OSError(errno.EIO)

    @staticmethod
    def _check_brightness(level):
        if not isinstance(level, int) or not 0 <= level <= 16:
            raise ValueError("brightness must be an integer from 0 to 16")

    def brightness(self, level):
        """Set global brightness: 0 is off, 1–16 are PWM duty steps."""
        self._check_brightness(level)
        self._write(bytes((0xAF + level, 0x83)) if level else b"\x82")

    def show(self):
        """Send the complete image to display RAM in one I2C transaction."""
        pixels = self._pixels
        packet = self._packet
        # CoreMatrix packs each group of eight horizontal pixels as two
        # nibbles, with the first four pixels in the high nibble.
        for i in range(32):
            value = pixels[i]
            packet[i + 1] = ((value & 0x0F) << 4) | (value >> 4)
        self._write(packet)

    def deinit(self):
        """Turn the display and oscillator off without changing the GPIO rail."""
        self._write(b"\x82\x80")
