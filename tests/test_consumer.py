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

from octobot_channels import InternalConsumer
from octobot_channels.channels import Channel, get_chan, del_chan, set_chan
from octobot_channels.util import create_channel_instance
from tests import TEST_CHANNEL, EmptyTestProducer


@pytest.mark.asyncio
async def test_internal_consumer():
    class TestInternalConsumer(InternalConsumer):
        async def perform(self):
            await get_chan(TEST_CHANNEL).stop()

    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer
        CONSUMER_CLASS = TestInternalConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    await get_chan(TEST_CHANNEL).new_consumer(internal_consumer=TestInternalConsumer())
    await get_chan(TEST_CHANNEL).get_internal_producer().send({})
