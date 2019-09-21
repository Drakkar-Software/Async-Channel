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
import asyncio

from octobot_channels.channels.channel import Channel

from octobot_channels.consumer import Consumer
from octobot_channels.producer import Producer

TEST_CHANNEL = "Test"
EMPTY_TEST_CHANNEL = "EmptyTest"
CONSUMER_KEY = "test"


class EmptyTestConsumer(Consumer):
    pass


class EmptyTestProducer(Producer):
    async def start(self):
        await asyncio.sleep(100000)

    async def pause(self, **kwargs):
        pass

    async def resume(self, **kwargs):
        pass


class EmptyTestChannel(Channel):
    CONSUMER_CLASS = EmptyTestConsumer
    PRODUCER_CLASS = EmptyTestProducer


async def empty_test_callback():
    pass


async def mock_was_called_once(mocked_method):
    await asyncio.sleep(0.1)
    mocked_method.assert_called_once()
