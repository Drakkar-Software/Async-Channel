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

import timy

import async_channel.constants
import async_channel.channels as channels
import async_channel.consumer as channel_consumer
import async_channel.util as util

import tests


async def ipc_channel():
    class BenchIPCConsumer(channel_consumer.Consumer):
        async def perform(self, data):
            pass

    class BenchIPCChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestProducer
        CONSUMER_CLASS = BenchIPCConsumer

        def __init__(self, use_ipc=True, ipc_url=async_channel.constants.DEFAULT_IPC_URL):
            super().__init__(use_ipc, ipc_url)

    channels.del_chan("BenchIPC")
    await util.create_channel_instance(BenchIPCChannel, channels.set_chan)
    producer = tests.EmptyTestProducer(channels.get_chan("BenchIPC"))
    await producer.run()
    await channels.get_chan("BenchIPC").new_consumer(tests.empty_test_callback)

    @timy.timer(loops=5000000)
    async def ipc_channel_send():
        await producer.send({'data': "Test"})

    await ipc_channel_send()


async def in_memory_channel():
    class InMemoryConsumer(channel_consumer.Consumer):
        async def perform(self, data):
            pass

    class InMemoryChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestProducer
        CONSUMER_CLASS = InMemoryConsumer

    channels.del_chan("InMemory")
    await util.create_channel_instance(InMemoryChannel, channels.set_chan)
    producer = tests.EmptyTestProducer(channels.get_chan("InMemory"))
    await producer.run()
    await channels.get_chan("InMemory").new_consumer(tests.empty_test_callback)

    @timy.timer(loops=5000000)
    async def in_memory_channel_send():
        await producer.send({'data': "Test"})

    await in_memory_channel_send()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(ipc_channel())
    # asyncio.get_event_loop().run_until_complete(in_memory_channel())
