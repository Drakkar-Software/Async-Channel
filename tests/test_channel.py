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
from octobot_channels.util import create_channel_instance

from octobot_channels.channels import Channel, get_chan, del_chan, set_chan
from tests import TEST_CHANNEL, EMPTY_TEST_CHANNEL, EmptyTestChannel, empty_test_callback, EmptyTestConsumer, \
    EmptyTestProducer


@pytest.mark.asyncio
async def test_get_chan():
    class TestChannel(Channel):
        pass

    del_chan(TEST_CHANNEL)
    await create_channel_instance(TestChannel, set_chan)
    await get_chan(TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_new_consumer_without_producer():
    del_chan(EMPTY_TEST_CHANNEL)
    await create_channel_instance(EmptyTestChannel, set_chan)
    await get_chan(EMPTY_TEST_CHANNEL).new_consumer(empty_test_callback)
    assert len(get_chan(EMPTY_TEST_CHANNEL).consumers) == 1
    await get_chan(EMPTY_TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_new_consumer_without_filters():
    del_chan(EMPTY_TEST_CHANNEL)
    await create_channel_instance(EmptyTestChannel, set_chan)
    consumer = await get_chan(EMPTY_TEST_CHANNEL).new_consumer(empty_test_callback)
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumers() == [consumer]
    await get_chan(EMPTY_TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_new_consumer_with_filters():
    del_chan(EMPTY_TEST_CHANNEL)
    await create_channel_instance(EmptyTestChannel, set_chan)
    consumer = await get_chan(EMPTY_TEST_CHANNEL).new_consumer(empty_test_callback, {"test_key": 1})
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumers() == [consumer]
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumer_from_filters({}) == []
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumer_from_filters({"test_key": 2}) == []
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumer_from_filters({"test_key": 1, "test2": 2}) == []
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumer_from_filters({"test_key": 1}) == [consumer]
    await get_chan(EMPTY_TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_remove_consumer():
    del_chan(EMPTY_TEST_CHANNEL)
    await create_channel_instance(EmptyTestChannel, set_chan)
    consumer = await get_chan(EMPTY_TEST_CHANNEL).new_consumer(empty_test_callback)
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumers() == [consumer]
    await get_chan(EMPTY_TEST_CHANNEL).remove_consumer(consumer)
    assert get_chan(EMPTY_TEST_CHANNEL).get_consumers() == []
    await get_chan(EMPTY_TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_unregister_producer():
    del_chan(EMPTY_TEST_CHANNEL)
    await create_channel_instance(EmptyTestChannel, set_chan)
    assert get_chan(EMPTY_TEST_CHANNEL).producers == []
    producer = EmptyTestProducer(None)
    await get_chan(EMPTY_TEST_CHANNEL).register_producer(producer)
    assert get_chan(EMPTY_TEST_CHANNEL).producers == [producer]
    await get_chan(EMPTY_TEST_CHANNEL).stop()


@pytest.mark.asyncio
async def test_register_producer():
    del_chan(EMPTY_TEST_CHANNEL)
    await create_channel_instance(EmptyTestChannel, set_chan)
    assert get_chan(EMPTY_TEST_CHANNEL).producers == []
    producer = EmptyTestProducer(None)
    await get_chan(EMPTY_TEST_CHANNEL).register_producer(producer)
    assert get_chan(EMPTY_TEST_CHANNEL).producers == [producer]
    get_chan(EMPTY_TEST_CHANNEL).unregister_producer(producer)
    assert get_chan(EMPTY_TEST_CHANNEL).producers == []
    await get_chan(EMPTY_TEST_CHANNEL).stop()
