"""
Module for managing an DPT Controlled remote value.

DPT 3.xxx.
"""

from enum import Enum

from xknx.exceptions import ConversionError, CouldNotParseTelegram
from xknx.knx import DPTBinary

from .remote_value import RemoteValue


class RemoteValueControlled(RemoteValue):
    """Abstraction for remote value of KNX DPT 3.xxx / DPT_Controlled_xxxx."""

    class Command(Enum):
        """Enum for the different KNX Controlled commands (directions)."""

        STOP = "Stop"
        UP = "Up"
        DOWN = "Down"

    def __init__(self,
                 xknx,
                 group_address=None,
                 device_name=None,
                 after_update_cb=None):
        """Initialize remote value of KNX DPT 3.xxx."""
        # pylint: disable=too-many-arguments
        super(RemoteValueControlled, self).__init__(
            xknx, group_address, None,
            device_name=device_name, after_update_cb=after_update_cb)

    def payload_valid(self, payload):
        """Test if telegram payload may be parsed."""
        return isinstance(payload, DPTBinary)

    def to_knx(self, value):
        """Convert value to payload."""
        if not isinstance(value, dict):
            raise ConversionError("value invalid", values=value)
        command = value.get('command')
        speed = value.get('speed')
        if command == self.Command.STOP:
            return DPTBinary(0)
        if not 0 <= speed <= 7:
            raise ConversionError("value invalid", values=value)
        if command == self.Command.UP:
            return DPTBinary(0x08 | speed)
        if command == self.Command.DOWN:
            return DPTBinary(speed)
        raise ConversionError("value invalid ", values=value)

    def from_knx(self, payload):
        """Convert current payload to value."""
        if not isinstance(payload, DPTBinary):
            raise CouldNotParseTelegram("payload invalid", payload=payload, device_name=self.device_name)

        value = payload.value
        if value & 0xf0:
            raise CouldNotParseTelegram("payload invalid", payload=payload, device_name=self.device_name)
        speed = value & 0x07
        direction = (value & 0x08) >> 3
        if speed == 0:
            command = self.Command.STOP
        elif direction == 1:
            command = self.Command.UP
        else:
            command = self.Command.DOWN
        return {
            'command': command,
            'speed': speed
        }

    async def start_downwards(self, speed):
        """Start moving down."""
        await self.set({
            'command': self.Command.DOWN,
            'speed': speed
        })

    async def start_upwards(self, speed):
        """Start moving up."""
        await self.set({
            'command': self.Command.UP,
            'speed': speed
        })

    async def stop(self):
        """Stop moving."""
        await self.set({
            'command': self.Command.STOP
        })
