"""Unit test for RemoteValueControlled objects."""
import asyncio
import unittest

from xknx import XKNX
from xknx.knx import DPTArray, DPTBinary, Telegram, GroupAddress
from xknx.exceptions import ConversionError, CouldNotParseTelegram
from xknx.devices import RemoteValueControlled


class TestRemoteValueControlled(unittest.TestCase):
    """Test class for RemoteValueControlled objects."""

    def setUp(self):
        """Set up test class."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        """Tear down test class."""
        self.loop.close()

    def test_to_knx(self):
        """Test to_knx function with normal operation."""
        xknx = XKNX(loop=self.loop)
        remote_value = RemoteValueControlled(xknx)

        stop = {
            'command': RemoteValueControlled.Command.STOP
        }
        self.assertEqual(remote_value.to_knx(stop), DPTBinary(0x00))

        up = {
            'command': RemoteValueControlled.Command.UP,
            'speed': 7
        }
        self.assertEqual(remote_value.to_knx(up), DPTBinary(0x0f))

        down = {
            'command': RemoteValueControlled.Command.DOWN,
            'speed': 7
        }
        self.assertEqual(remote_value.to_knx(down), DPTBinary(0x07))

    def test_from_knx(self):
        """Test from_knx function with normal operation."""
        xknx = XKNX(loop=self.loop)
        remote_value = RemoteValueControlled(xknx)
        stop = {
            'command': RemoteValueControlled.Command.STOP,
            'speed': 0
        }
        self.assertEqual(remote_value.from_knx(DPTBinary(0x00)), stop)
        self.assertEqual(remote_value.from_knx(DPTBinary(0x08)), stop)

        up = {
            'command': RemoteValueControlled.Command.UP,
            'speed': 1
        }
        self.assertEqual(remote_value.from_knx(DPTBinary(0x09)), up)

        down = {
            'command': RemoteValueControlled.Command.DOWN,
            'speed': 1
        }
        self.assertEqual(remote_value.from_knx(DPTBinary(0x01)), down)

    def test_to_knx_error(self):
        """Test to_knx function with wrong parametern."""
        xknx = XKNX(loop=self.loop)
        remote_value = RemoteValueControlled(xknx)
        with self.assertRaises(ConversionError):
            remote_value.to_knx(8)

    def test_set(self):
        """Test setting value."""
        xknx = XKNX(loop=self.loop)
        remote_value = RemoteValueControlled(
            xknx,
            group_address=GroupAddress("1/2/3"))
        self.loop.run_until_complete(asyncio.Task(remote_value.start_upwards(7)))
        self.assertEqual(xknx.telegrams.qsize(), 1)
        telegram = xknx.telegrams.get_nowait()
        self.assertEqual(
            telegram,
            Telegram(
                GroupAddress('1/2/3'),
                payload=DPTBinary(0x0f)))
        self.loop.run_until_complete(asyncio.Task(remote_value.stop()))
        self.assertEqual(xknx.telegrams.qsize(), 1)
        telegram = xknx.telegrams.get_nowait()
        self.assertEqual(
            telegram,
            Telegram(
                GroupAddress('1/2/3'),
                payload=DPTBinary(0x00)))

    def test_process(self):
        """Test process telegram."""
        xknx = XKNX(loop=self.loop)
        remote_value = RemoteValueControlled(
            xknx,
            group_address=GroupAddress("1/2/3"))
        telegram = Telegram(
            group_address=GroupAddress("1/2/3"),
            payload=DPTBinary(0x05))
        self.assertEqual(remote_value.value, None)
        self.loop.run_until_complete(asyncio.Task(remote_value.process(telegram)))
        self.assertEqual(remote_value.value, {
            'command': RemoteValueControlled.Command.DOWN,
            'speed': 5
        })

    def test_to_process_error(self):
        """Test process erroneous telegram."""
        xknx = XKNX(loop=self.loop)
        remote_value = RemoteValueControlled(
            xknx,
            group_address=GroupAddress("1/2/3"))
        with self.assertRaises(CouldNotParseTelegram):
            telegram = Telegram(
                group_address=GroupAddress("1/2/3"),
                payload=DPTArray((0x01)))
            self.loop.run_until_complete(asyncio.Task(remote_value.process(telegram)))
        # with self.assertRaises(CouldNotParseTelegram):
        #     telegram = Telegram(
        #         group_address=GroupAddress("1/2/3"),
        #         payload=DPTBinary(0xff))
        #     self.loop.run_until_complete(asyncio.Task(remote_value.process(telegram)))
