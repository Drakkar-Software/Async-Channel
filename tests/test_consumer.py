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
from mock import AsyncMock, patch

from octobot_channels.consumer import InternalConsumer, SupervisedConsumer
from octobot_channels.channels.channel import Channel, get_chan, del_chan, set_chan
from octobot_channels.util.channel_creator import create_channel_instance
from tests import TEST_CHANNEL, EmptyTestProducer, empty_test_callback, EmptyTestConsumer, mock_was_called_once


async def init_consumer_test():
    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer
        CONSUMER_CLASS = EmptyTestConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    return await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)


@pytest.mark.asyncio
async def test_perform_called():
    consumer = await init_consumer_test()
    with patch.object(consumer, 'perform', new=AsyncMock()) as mocked_consume_ends:
        await get_chan(TEST_CHANNEL).get_internal_producer().send({})
        await mock_was_called_once(mocked_consume_ends)

    await get_chan(TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_consume_ends_called():
    consumer = await init_consumer_test()
    with patch.object(consumer, 'consume_ends', new=AsyncMock()) as mocked_consume_ends:
        await get_chan(TEST_CHANNEL).get_internal_producer().send({})
        await mock_was_called_once(mocked_consume_ends)

    await get_chan(TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_internal_consumer():
    class TestInternalConsumer(InternalConsumer):
        async def perform(self, kwargs):
            pass

    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer
        CONSUMER_CLASS = TestInternalConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    consumer = TestInternalConsumer()
    await get_chan(TEST_CHANNEL).new_consumer(internal_consumer=consumer)

    with patch.object(consumer, 'perform', new=AsyncMock()) as mocked_consume_ends:
        await get_chan(TEST_CHANNEL).get_internal_producer().send({})
        await mock_was_called_once(mocked_consume_ends)

    await get_chan(TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_supervised_consumer():
    class TestSupervisedConsumer(SupervisedConsumer):
        pass

    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer
        CONSUMER_CLASS = TestSupervisedConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    consumer = await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)
    await get_chan(TEST_CHANNEL).get_internal_producer().send({})
    await consumer.queue.join()
    await get_chan(TEST_CHANNEL).stop()
