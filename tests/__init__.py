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

from octobot_channels import Producer, Consumer
from octobot_channels.channels import Channel

TEST_CHANNEL = "Test"
EMPTY_TEST_CHANNEL = "EmptyTest"
CONSUMER_KEY = "test"


class EmptyTestConsumer(Consumer):
    pass


class EmptyTestProducer(Producer):
    async def start(self):
        await asyncio.sleep(100000)


class EmptyTestChannel(Channel):
    CONSUMER_CLASS = EmptyTestConsumer
    PRODUCER_CLASS = EmptyTestProducer


async def empty_test_callback():
    pass
