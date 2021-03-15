#  Drakkar-Software Async-Channel
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

import pytest

import async_channel.consumers as channel_consumer
import async_channel.channels as channels
import async_channel.producers as channel_producer
import async_channel.util as util
import tests

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


async def test_send_ipc_internal_producer_without_consumer():
    class TestIPCProducer(channel_producer.IPCProducer):
        async def send(self, data, **kwargs):
            await super().send(data)
            await channels.get_chan(tests.TEST_IPC_CHANNEL).stop()

        async def pause(self):
            pass

        async def resume(self):
            pass

    class TestIPCChannel(channels.Channel):
        PRODUCER_CLASS = TestIPCProducer

    channels.del_chan(tests.TEST_IPC_CHANNEL)
    await util.create_channel_instance(TestIPCChannel, channels.set_chan)
    await channels.get_chan(tests.TEST_IPC_CHANNEL).get_internal_producer().send({})


async def test_send_ipc_producer_with_consumer():
    class TestIPCConsumer(channel_consumer.IPCConsumer):
        pass

    class TestIPCChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestIPCProducer
        CONSUMER_CLASS = TestIPCConsumer

    async def callback(data):
        assert data == "test"
        await channels.get_chan(tests.TEST_IPC_CHANNEL).stop()

    channels.del_chan(tests.TEST_IPC_CHANNEL)
    await util.create_channel_instance(TestIPCChannel, channels.set_chan)
    await channels.get_chan(tests.TEST_IPC_CHANNEL).new_consumer(callback)

    producer = tests.EmptyTestIPCProducer(channels.get_chan(tests.TEST_IPC_CHANNEL))
    await producer.run()
    await producer.send({"data": "test"})
    await asyncio.sleep(5)  # wait for socket to close


async def test_send_ipc_producer_with_multiple_consumers():
    class TestIPCConsumer(channel_consumer.IPCConsumer):
        pass

    class TestIPCChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestIPCProducer
        CONSUMER_CLASS = TestIPCConsumer

    async def callback(data):
        assert data == "test"
        await channels.get_chan(tests.TEST_IPC_CHANNEL).stop()

    channels.del_chan(tests.TEST_IPC_CHANNEL)
    await util.create_channel_instance(TestIPCChannel, channels.set_chan)
    consumer_1 = await channels.get_chan(tests.TEST_IPC_CHANNEL).new_consumer(callback)
    consumer_2 = await channels.get_chan(tests.TEST_IPC_CHANNEL).new_consumer(callback)

    assert consumer_1.queue.empty()
    assert consumer_2.queue.empty()

    producer = tests.EmptyTestIPCProducer(channels.get_chan(tests.TEST_IPC_CHANNEL))
    await producer.run()
    await producer.send({"data": "test"})


async def test_send_ipc_producer_with_multiple_consumers_and_filter():
    class TestIPCConsumer(channel_consumer.IPCConsumer):
        pass

    class TestIPCChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestIPCProducer
        CONSUMER_CLASS = TestIPCConsumer

    async def callback(data):
        assert data == "test"
        await channels.get_chan(tests.TEST_IPC_CHANNEL).stop()

    channels.del_chan(tests.TEST_IPC_CHANNEL)
    await util.create_channel_instance(TestIPCChannel, channels.set_chan)
    consumer_1 = await channels.get_chan(tests.TEST_IPC_CHANNEL).new_consumer(callback)
    consumer_2 = await channels.get_chan(tests.TEST_IPC_CHANNEL).new_consumer(callback)

    assert consumer_1.queue.empty()
    assert consumer_2.queue.empty()

    producer = tests.EmptyTestIPCProducer(channels.get_chan(tests.TEST_IPC_CHANNEL))
    await producer.run()
    await producer.send({"data": "test"}, consumers=[consumer_1])  # same as consumers=None
