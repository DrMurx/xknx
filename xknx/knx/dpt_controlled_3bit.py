"""Implementation of KNX 4 bit control data point."""

from enum import Enum

from xknx.exceptions import ConversionError

from .dpt import DPTBase


class DPTControlCommand(Enum):
    """Enum for the different KNX Controlled commands (directions)."""

    STOP = "Stop"
    UP = "Up"
    DOWN = "Down"


class DPTControlled3Bit(DPTBase):
    """
    Abstraction for KNX 4 bit control data point.

    Used for dimming or blinds

    DPT 3.xxx
    """

    @classmethod
    def from_knx(cls, raw):
        """Parse/deserialize from KNX/IP raw data."""
        cls.test_bytesarray(raw, 1)

        value = raw[0]

        if value & 0xf0:
            raise ConversionError("Can't parse DPTControl3Bit", value=value)
        speed = value & 0x07
        direction = (value & 0x08) >> 3
        if speed == 0:
            command = DPTControlCommand.STOP
        elif direction == 1:
            command = DPTControlCommand.UP
        else:
            command = DPTControlCommand.DOWN
        return {
            'command': command,
            'speed': speed
        }

    @classmethod
    def to_knx(cls, values):
        """Serialize to KNX/IP raw data from dict with elements command and speed."""
        if not isinstance(values, dict):
            raise ConversionError("Can't serialize DPTControl3Bit", values=values)
        command = values.get('command')
        speed = values.get('speed')
        if command == DPTControlCommand.STOP:
            return (0,)
        if not 0 <= speed <= 7:
            raise ConversionError("Can't serialize DPTControl3Bit", values=values)
        if command == DPTControlCommand.UP:
            return (0x08 | speed,)
        if command == DPTControlCommand.DOWN:
            return (speed,)
        raise ConversionError("Could not parse DPTControlCommand", values=values)
