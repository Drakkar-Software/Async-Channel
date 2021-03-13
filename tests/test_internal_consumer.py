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

import pytest
import mock 

import async_channel.consumers as consumers
import async_channel.channels as channels
import async_channel.util as util
import tests


@pytest.fixture
async def internal_consumer():
    class TestInternalConsumer(consumers.InternalConsumer):
        async def perform(self, kwargs):
            pass

    class TestChannel(channels.Channel):
        PRODUCER_CLASS = tests.EmptyTestProducer
        CONSUMER_CLASS = TestInternalConsumer

    channels.del_chan(tests.TEST_CHANNEL)
    await util.create_channel_instance(TestChannel, channels.set_chan)
    producer = tests.EmptyTestProducer(channels.get_chan(tests.TEST_CHANNEL))
    await producer.run()
    yield TestInternalConsumer(channels.get_chan(tests.TEST_CHANNEL))
    await channels.get_chan(tests.TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_internal_consumer(internal_consumer):
    await channels.get_chan(tests.TEST_CHANNEL).new_consumer(internal_consumer=internal_consumer)

    with mock.patch.object(internal_consumer, 'perform', new=mock.AsyncMock()) as mocked_consume_ends:
        await channels.get_chan(tests.TEST_CHANNEL).get_internal_producer().send({})
        await tests.mock_was_called_once(mocked_consume_ends)


@pytest.mark.asyncio
async def test_default_internal_consumer_callback(internal_consumer):
    with pytest.raises(NotImplementedError):
        await internal_consumer.internal_callback()
