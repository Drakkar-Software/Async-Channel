#  Drakkar-Software OctoBot-Channels
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.

import pytest

from octobot_channels.channels import Channel, get_chan, del_chan, set_chan, ChannelInstances
from octobot_channels.util import create_channel_instance, create_all_subclasses_channel
from tests import TEST_CHANNEL


@pytest.mark.asyncio
async def test_create_channel_instance():
    class TestChannel(Channel):
        pass

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    await get_chan(TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_create_all_subclasses_channel():
    class TestChannelClass(Channel):
        pass

    class Test1Channel(TestChannelClass):
        pass

    class Test2Channel(TestChannelClass):
        pass

    del_chan(TEST_CHANNEL)
    await create_all_subclasses_channel(TestChannelClass, set_chan)
    assert len(ChannelInstances.instance().channels) == 3  # (EmptyTestChannel, Test1Channel, Test2Channel)
