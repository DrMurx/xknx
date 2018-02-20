"""Unit test for KNX 4 bit control data point objects."""
import unittest
from unittest.mock import patch
import struct

from xknx.exceptions import ConversionError
from xknx.knx import DPTControlCommand, DPTControlled3Bit


class TestDPTControlled3Bit(unittest.TestCase):
    """Test class for KNX 4 bit control data point object."""

    # pylint: disable=too-many-public-methods,invalid-name

    def test_from_knx_up(self):
        """."""
        self.assertEqual(DPTControlled3Bit().from_knx((0x09,)), {
            'command': DPTControlCommand.UP,
            'speed': 1
        })
        self.assertEqual(DPTControlled3Bit().from_knx((0x0f,)), {
            'command': DPTControlCommand.UP,
            'speed': 7
        })

    def test_to_knx_up(self):
        """."""
        raw = {
            'command': DPTControlCommand.UP,
            'speed': 1
        }
        self.assertEqual(DPTControlled3Bit().to_knx(raw), (0x09,))
        raw = {
            'command': DPTControlCommand.UP,
            'speed': 7
        }
        self.assertEqual(DPTControlled3Bit().to_knx(raw), (0x0f,))

    def test_from_knx_down(self):
        """."""
        self.assertEqual(DPTControlled3Bit().from_knx((0x01,)), {
            'command': DPTControlCommand.DOWN,
            'speed': 1
        })
        self.assertEqual(DPTControlled3Bit().from_knx((0x07,)), {
            'command': DPTControlCommand.DOWN,
            'speed': 7
        })

    def test_down_to_knx(self):
        """."""
        raw = {
            'command': DPTControlCommand.DOWN,
            'speed': 1
        }
        self.assertEqual(DPTControlled3Bit().to_knx(raw), (0x01,))
        raw = {
            'command': DPTControlCommand.DOWN,
            'speed': 7
        }
        self.assertEqual(DPTControlled3Bit().to_knx(raw), (0x07,))

    def test_from_knx_stop(self):
        """."""
        self.assertEqual(DPTControlled3Bit().from_knx((0x00,)), {
            'command': DPTControlCommand.STOP,
            'speed': 0
        })

    def test_from_knx_stop_ignore_direction(self):
        """."""
        self.assertEqual(DPTControlled3Bit().from_knx((0x08,)), {
            'command': DPTControlCommand.STOP,
            'speed': 0
        })

    def test_to_knx_stop(self):
        """."""
        raw = {
            'command': DPTControlCommand.STOP
        }
        self.assertEqual(DPTControlled3Bit().to_knx(raw), (0x00,))

    def test_to_knx_stop_ignore_speed(self):
        """."""
        raw = {
            'command': DPTControlCommand.STOP,
            'speed': 7
        }
        self.assertEqual(DPTControlled3Bit().to_knx(raw), (0x00,))

    #
    # TEST WRONG KNX
    #
    def test_from_knx_wrong_size(self):
        """Test parsing of DPTControlled3Bit from KNX with wrong binary values (wrong size)."""
        with self.assertRaises(ConversionError):
            DPTControlled3Bit().from_knx((0xF8, 0x23))

    def test_from_knx_wrong_bytes(self):
        """Test parsing of DPTControlled3Bit with wrong binary values."""
        with self.assertRaises(ConversionError):
            DPTControlled3Bit().from_knx((0x1f,))

    #
    # TEST WRONG PARAMETER
    #
    def test_to_knx_wrong_parameter(self):
        """Test parsing from DPTControlled3Bit object from wrong string value."""
        with self.assertRaises(ConversionError):
            DPTControlled3Bit().to_knx("hello")

    def test_to_knx_wrong_command(self):
        """Test parsing from DPTControlled3Bit object with invalid command."""
        raw = {
            'command': "up",
            'speed': 1
        }
        with self.assertRaises(ConversionError):
            DPTControlled3Bit().to_knx(raw)

    def test_to_knx_wrong_speed(self):
        """Test parsing from DPTControlled3Bit object with invalid speed."""
        raw = {
            'command': DPTControlCommand.DOWN,
            'speed': 8
        }
        with self.assertRaises(ConversionError):
            DPTControlled3Bit().to_knx(raw)

    def test_to_knx_negative_speed(self):
        """Test parsing from DPTControlled3Bit object with invalid speed."""
        raw = {
            'command': DPTControlCommand.DOWN,
            'speed': -1
        }
        with self.assertRaises(ConversionError):
            DPTControlled3Bit().to_knx(raw)
