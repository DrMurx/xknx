"""Example for switching a light on and off."""
import asyncio

from xknx import XKNX
from xknx.devices import Light


async def main():
    """Connect to KNX/IP bus, dimm up fast and down slow, set it off again afterwards."""
    xknx = XKNX()
    await xknx.start()

    light = Light(xknx,
                  name='TestLight2',
                  group_address_switch='1/0/12',
                  group_address_dimm='1/0/14')

    await light.start_dimming_up(3)
    await asyncio.sleep(1)
    await light.stop_dimming()
    await asyncio.sleep(1)
    await light.start_dimming_down(1)
    await asyncio.sleep(1)
    await light.stop_dimming()

    await light.set_off()

    await xknx.stop()


# pylint: disable=invalid-name
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
