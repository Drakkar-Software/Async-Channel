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
from octobot_channels.consumer import Consumer, SupervisedConsumer

from octobot_channels.channels.channel import Channel, get_chan, del_chan, set_chan
from octobot_channels.producer import Producer
from octobot_channels.util import create_channel_instance
from tests import EmptyTestConsumer, TEST_CHANNEL, empty_test_callback, EmptyTestProducer


@pytest.mark.asyncio
async def test_send_internal_producer_without_consumer():
    class TestProducer(Producer):
        async def send(self, data, **kwargs):
            await super().send(data)
            await get_chan(TEST_CHANNEL).stop()

        async def pause(self):
            pass

        async def resume(self):
            pass

    class TestChannel(Channel):
        PRODUCER_CLASS = TestProducer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    await get_chan(TEST_CHANNEL).get_internal_producer().send({})


@pytest.mark.asyncio
async def test_send_producer_without_consumer():
    class TestProducer(Producer):
        async def send(self, data, **kwargs):
            await super().send(data)
            await get_chan(TEST_CHANNEL).stop()

        async def pause(self):
            pass

        async def resume(self):
            pass

    class TestConsumer(Consumer):
        async def consume(self):
            while not self.should_stop:
                await self.callback(**(await self.queue.get()))

    class TestChannel(Channel):
        PRODUCER_CLASS = TestProducer
        CONSUMER_CLASS = TestConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)

    producer = TestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    await producer.send({})


@pytest.mark.asyncio
async def test_send_producer_with_consumer():
    class TestConsumer(Consumer):
        pass

    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer
        CONSUMER_CLASS = TestConsumer

    async def callback(data):
        assert data == "test"
        await get_chan(TEST_CHANNEL).stop()

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    await get_chan(TEST_CHANNEL).new_consumer(callback)

    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    await producer.send({"data": "test"})


@pytest.mark.asyncio
async def test_pause_producer_without_consumers():
    class TestProducer(Producer):
        async def pause(self):
            await get_chan(TEST_CHANNEL).stop()

        async def pause(self):
            pass

        async def resume(self):
            pass

    class TestChannel(Channel):
        PRODUCER_CLASS = TestProducer
        CONSUMER_CLASS = EmptyTestConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    await TestProducer(get_chan(TEST_CHANNEL)).run()


@pytest.mark.asyncio
async def test_pause_producer_with_removed_consumer():
    class TestProducer(Producer):
        async def pause(self):
            await get_chan(TEST_CHANNEL).stop()

        async def pause(self):
            pass

        async def resume(self):
            pass

    class TestChannel(Channel):
        PRODUCER_CLASS = TestProducer
        CONSUMER_CLASS = EmptyTestConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    consumer = await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)
    await TestProducer(get_chan(TEST_CHANNEL)).run()
    await get_chan(TEST_CHANNEL).remove_consumer(consumer)


@pytest.mark.asyncio
async def test_resume_producer():
    class TestProducer(Producer):
        async def resume(self):
            await get_chan(TEST_CHANNEL).stop()

        async def pause(self):
            pass

        async def resume(self):
            pass

    class TestChannel(Channel):
        PRODUCER_CLASS = TestProducer
        CONSUMER_CLASS = EmptyTestConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    await TestProducer(get_chan(TEST_CHANNEL)).run()
    await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)


@pytest.mark.asyncio
async def test_resume_producer():
    class TestSupervisedConsumer(SupervisedConsumer):
        pass

    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer
        CONSUMER_CLASS = TestSupervisedConsumer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    await producer.run()
    await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)
    await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)
    await get_chan(TEST_CHANNEL).new_consumer(empty_test_callback)
    await producer.send({"data": "test"})
    await producer.wait_for_processing()
    await get_chan(TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_producer_is_running():
    class TestChannel(Channel):
        PRODUCER_CLASS = EmptyTestProducer

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    producer = EmptyTestProducer(get_chan(TEST_CHANNEL))
    assert not producer.is_running
    await producer.run()
    assert producer.is_running
    await get_chan(TEST_CHANNEL).stop()
    assert not producer.is_running
