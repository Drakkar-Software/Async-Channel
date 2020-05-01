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
from mock import AsyncMock, patch
import pytest

from octobot_channels.channels.channel import Channel, get_chan, del_chan, set_chan
from octobot_channels.producer import Producer
from octobot_channels.util.channel_creator import create_channel_instance
from tests import EmptyTestConsumer, mock_was_called_once, mock_was_not_called

TEST_SYNCHRONIZED_CHANNEL = "TestSynchronized"


class TestSynchronizedProducer(Producer):
    async def send(self, data, **kwargs):
        await super().send(data)
        await get_chan(TEST_SYNCHRONIZED_CHANNEL).stop()

    async def pause(self):
        pass

    async def resume(self):
        pass


class TestSynchronizedChannel(Channel):
    PRODUCER_CLASS = TestSynchronizedProducer
    CONSUMER_CLASS = EmptyTestConsumer


@pytest.yield_fixture()
async def synchronized_channel():
    yield await create_channel_instance(TestSynchronizedChannel, set_chan, is_synchronized=True)
    del_chan(TEST_SYNCHRONIZED_CHANNEL)


@pytest.mark.asyncio
async def test_producer_synchronized_perform_consumers_queue_with_one_consumer(synchronized_channel):
    async def callback():
        pass

    test_consumer = await synchronized_channel.new_consumer(callback)

    producer = TestSynchronizedProducer(get_chan(TEST_SYNCHRONIZED_CHANNEL))
    await producer.run()

    with patch.object(test_consumer, 'callback', new=AsyncMock()) as mocked_test_consumer_callback:
        await producer.send({})
        await mock_was_not_called(mocked_test_consumer_callback)
        await producer.synchronized_perform_consumers_queue(1)
        await mock_was_called_once(mocked_test_consumer_callback)


@pytest.mark.asyncio
async def test_synchronized_no_tasks(synchronized_channel):
    async def callback():
        pass

    test_consumer = await synchronized_channel.new_consumer(callback)

    producer = TestSynchronizedProducer(get_chan(TEST_SYNCHRONIZED_CHANNEL))
    await producer.run()

    assert test_consumer.consume_task is None
    assert producer.produce_task is None


@pytest.mark.asyncio
async def test_is_consumers_queue_empty_with_one_consumer(synchronized_channel):
    async def callback():
        pass

    await synchronized_channel.new_consumer(callback)

    producer = TestSynchronizedProducer(get_chan(TEST_SYNCHRONIZED_CHANNEL))
    await producer.run()

    await producer.send({})
    assert not producer.is_consumers_queue_empty(1)
    assert not producer.is_consumers_queue_empty(2)
    await producer.synchronized_perform_consumers_queue(1)
    assert producer.is_consumers_queue_empty(1)
    assert producer.is_consumers_queue_empty(2)


@pytest.mark.asyncio
async def test_is_consumers_queue_empty_with_multiple_consumers(synchronized_channel):
    async def callback():
        pass

    await synchronized_channel.new_consumer(callback)
    await synchronized_channel.new_consumer(callback)
    await synchronized_channel.new_consumer(callback, priority_level=2)
    await synchronized_channel.new_consumer(callback, priority_level=2)
    await synchronized_channel.new_consumer(callback, priority_level=3)

    producer = TestSynchronizedProducer(get_chan(TEST_SYNCHRONIZED_CHANNEL))
    await producer.run()

    await producer.send({})
    assert not producer.is_consumers_queue_empty(1)
    assert not producer.is_consumers_queue_empty(2)
    assert not producer.is_consumers_queue_empty(3)
    await producer.synchronized_perform_consumers_queue(1)
    assert producer.is_consumers_queue_empty(1)
    assert not producer.is_consumers_queue_empty(2)
    assert not producer.is_consumers_queue_empty(3)
    await producer.synchronized_perform_consumers_queue(2)
    assert producer.is_consumers_queue_empty(1)
    assert producer.is_consumers_queue_empty(2)
    assert not producer.is_consumers_queue_empty(3)
    await producer.synchronized_perform_consumers_queue(2)
    assert not producer.is_consumers_queue_empty(3)
    await producer.synchronized_perform_consumers_queue(3)
    assert producer.is_consumers_queue_empty(3)


@pytest.mark.asyncio
async def test_producer_synchronized_perform_consumers_queue_with_multiple_consumer(synchronized_channel):
    async def callback():
        pass

    test_consumer_1_1 = await synchronized_channel.new_consumer(callback)
    test_consumer_1_2 = await synchronized_channel.new_consumer(callback)
    test_consumer_2_1 = await synchronized_channel.new_consumer(callback, priority_level=2)
    test_consumer_2_2 = await synchronized_channel.new_consumer(callback, priority_level=2)
    test_consumer_3_1 = await synchronized_channel.new_consumer(callback, priority_level=3)

    producer = TestSynchronizedProducer(get_chan(TEST_SYNCHRONIZED_CHANNEL))
    await producer.run()

    with patch.object(test_consumer_1_1, 'callback', new=AsyncMock()) as mocked_test_consumer_1_1_callback, \
            patch.object(test_consumer_1_2, 'callback', new=AsyncMock()) as mocked_test_consumer_1_2_callback, \
            patch.object(test_consumer_2_1, 'callback', new=AsyncMock()) as mocked_test_consumer_2_1_callback, \
            patch.object(test_consumer_2_2, 'callback', new=AsyncMock()) as mocked_test_consumer_2_2_callback, \
            patch.object(test_consumer_3_1, 'callback', new=AsyncMock()) as mocked_test_consumer_3_1_callback:
        await producer.send({})
        await mock_was_not_called(mocked_test_consumer_1_1_callback)
        await mock_was_not_called(mocked_test_consumer_1_2_callback)
        await mock_was_not_called(mocked_test_consumer_2_1_callback)
        await mock_was_not_called(mocked_test_consumer_2_2_callback)
        await mock_was_not_called(mocked_test_consumer_3_1_callback)
        await producer.synchronized_perform_consumers_queue(1)
        await mock_was_called_once(mocked_test_consumer_1_1_callback)
        await mock_was_called_once(mocked_test_consumer_1_2_callback)
        await mock_was_not_called(mocked_test_consumer_2_1_callback)
        await mock_was_not_called(mocked_test_consumer_2_2_callback)
        await mock_was_not_called(mocked_test_consumer_3_1_callback)
        await producer.synchronized_perform_consumers_queue(2)
        await mock_was_called_once(mocked_test_consumer_1_1_callback)
        await mock_was_called_once(mocked_test_consumer_1_2_callback)
        await mock_was_called_once(mocked_test_consumer_2_1_callback)
        await mock_was_called_once(mocked_test_consumer_2_2_callback)
        await mock_was_not_called(mocked_test_consumer_3_1_callback)
        assert not producer.is_consumers_queue_empty(3)
        await producer.synchronized_perform_consumers_queue(3)
        await mock_was_called_once(mocked_test_consumer_3_1_callback)
        assert producer.is_consumers_queue_empty(1)
        assert producer.is_consumers_queue_empty(2)
        assert producer.is_consumers_queue_empty(3)

    with patch.object(test_consumer_1_1, 'callback', new=AsyncMock()) as mocked_test_consumer_1_1_callback, \
            patch.object(test_consumer_1_2, 'callback', new=AsyncMock()) as mocked_test_consumer_1_2_callback, \
            patch.object(test_consumer_2_1, 'callback', new=AsyncMock()) as mocked_test_consumer_2_1_callback, \
            patch.object(test_consumer_2_2, 'callback', new=AsyncMock()) as mocked_test_consumer_2_2_callback, \
            patch.object(test_consumer_3_1, 'callback', new=AsyncMock()) as mocked_test_consumer_3_1_callback:
        await producer.send({})
        await mock_was_not_called(mocked_test_consumer_1_1_callback)
        await mock_was_not_called(mocked_test_consumer_1_2_callback)
        await mock_was_not_called(mocked_test_consumer_2_1_callback)
        await mock_was_not_called(mocked_test_consumer_2_2_callback)
        await mock_was_not_called(mocked_test_consumer_3_1_callback)
        assert not producer.is_consumers_queue_empty(2)
        await producer.synchronized_perform_consumers_queue(3)
        await mock_was_called_once(mocked_test_consumer_1_1_callback)
        await mock_was_called_once(mocked_test_consumer_1_2_callback)
        await mock_was_called_once(mocked_test_consumer_2_1_callback)
        await mock_was_called_once(mocked_test_consumer_2_2_callback)
        await mock_was_called_once(mocked_test_consumer_3_1_callback)
        assert producer.is_consumers_queue_empty(1)
        assert producer.is_consumers_queue_empty(2)
        assert producer.is_consumers_queue_empty(3)
