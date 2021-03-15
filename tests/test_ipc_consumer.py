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

import mock
import pytest

import async_channel.channels as channels
import async_channel.util as util
import tests


async def init_ipc_consumer_test():
    class TestIPCChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestIPCProducer
        CONSUMER_CLASS = tests.EmptyTestIPCConsumer

    channels.del_chan(tests.TEST_IPC_CHANNEL)
    await util.create_channel_instance(TestIPCChannel, channels.set_chan)
    producer = tests.EmptyTestProducer(channels.get_chan(tests.TEST_IPC_CHANNEL))
    await producer.run()
    return await channels.get_chan(tests.TEST_IPC_CHANNEL).new_consumer(callback=tests.empty_test_callback)


@pytest.mark.asyncio
async def test_ipc_perform_called():
    consumer = await init_ipc_consumer_test()
    with mock.patch.object(consumer, 'perform', new=mock.AsyncMock()) as mocked_consume_ends:
        await channels.get_chan(tests.TEST_IPC_CHANNEL).get_internal_producer().send("test")
        await tests.mock_was_called_once(mocked_consume_ends)

    await channels.get_chan(tests.TEST_IPC_CHANNEL).stop()


@pytest.mark.asyncio
async def test_ipc_consume_ends_called():
    consumer = await init_ipc_consumer_test()
    with mock.patch.object(consumer, 'consume_ends', new=mock.AsyncMock()) as mocked_consume_ends:
        await channels.get_chan(tests.TEST_IPC_CHANNEL).get_internal_producer().send("test")
        await tests.mock_was_called_once(mocked_consume_ends)

    await channels.get_chan(tests.TEST_IPC_CHANNEL).stop()
