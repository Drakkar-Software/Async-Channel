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
from uuid import uuid4

import pytest

from octobot_channels.channels.channel_instances import del_chan_at_id, get_chan_at_id, set_chan_at_id, \
    del_channel_container, get_channels
from octobot_channels.util.channel_creator import create_channel_instance
from tests import EmptyTestWithIdChannel, EMPTY_TEST_WITH_ID_CHANNEL


@pytest.fixture()
async def chan_id():
    channel_uuid = uuid4().hex
    await create_channel_instance(EmptyTestWithIdChannel, set_chan_at_id, test_id=channel_uuid)
    return channel_uuid


@pytest.yield_fixture()
async def channel_id():
    channel_uuid = uuid4().hex
    await create_channel_instance(EmptyTestWithIdChannel, set_chan_at_id, test_id=channel_uuid)
    yield channel_uuid
    await get_chan_at_id(EMPTY_TEST_WITH_ID_CHANNEL, channel_uuid).stop()
    del_chan_at_id(EMPTY_TEST_WITH_ID_CHANNEL, channel_uuid)


@pytest.mark.asyncio
async def test_get_chan_at_id(channel_id):
    assert get_chan_at_id(EMPTY_TEST_WITH_ID_CHANNEL, channel_id)


@pytest.mark.asyncio
async def test_set_chan_at_id_already_exist(channel_id):
    with pytest.raises(ValueError):
        await create_channel_instance(EmptyTestWithIdChannel, set_chan_at_id, test_id=channel_id)


@pytest.mark.asyncio
async def test_del_channel_container_not_exist_does_not_raise(channel_id):
    del_channel_container(channel_id + "test")


@pytest.mark.asyncio
async def test_del_channel_container(chan_id):
    del_channel_container(chan_id)
    with pytest.raises(KeyError):
        get_chan_at_id(EMPTY_TEST_WITH_ID_CHANNEL, chan_id)
    del_chan_at_id(EMPTY_TEST_WITH_ID_CHANNEL, chan_id)


@pytest.mark.asyncio
async def test_get_channels_not_exist(channel_id):
    with pytest.raises(KeyError):
        get_channels(channel_id + "test")


@pytest.mark.asyncio
async def test_get_channels(chan_id):
    class EmptyTestWithId2Channel(EmptyTestWithIdChannel):
        pass

    class EmptyTestWithId3Channel(EmptyTestWithIdChannel):
        pass

    class EmptyTestWithId4Channel(EmptyTestWithIdChannel):
        pass

    class EmptyTestWithId5Channel(EmptyTestWithIdChannel):
        pass

    class EmptyTestWithId6Channel(EmptyTestWithIdChannel):
        pass

    channel_4_id = uuid4().hex
    channel_6_id = uuid4().hex
    ch1 = get_chan_at_id(EMPTY_TEST_WITH_ID_CHANNEL, chan_id)
    ch2 = await create_channel_instance(EmptyTestWithId2Channel, set_chan_at_id, test_id=chan_id)
    ch3 = await create_channel_instance(EmptyTestWithId3Channel, set_chan_at_id, test_id=chan_id)
    ch4 = await create_channel_instance(EmptyTestWithId4Channel, set_chan_at_id, test_id=channel_4_id)
    ch5 = await create_channel_instance(EmptyTestWithId5Channel, set_chan_at_id, test_id=channel_4_id)
    ch6 = await create_channel_instance(EmptyTestWithId6Channel, set_chan_at_id, test_id=channel_6_id)
    assert len(get_channels(chan_id)) == 3
    assert len(get_channels(channel_4_id)) == 2
    assert len(get_channels(channel_6_id)) == 1
    assert get_channels(chan_id) == {
        "EmptyTestWithId": ch1,
        "EmptyTestWithId2": ch2,
        "EmptyTestWithId3": ch3
    }
    assert get_channels(channel_4_id) == {
        "EmptyTestWithId4": ch4,
        "EmptyTestWithId5": ch5
    }
    assert get_channels(channel_6_id) == {
        "EmptyTestWithId6": ch6
    }
    del_channel_container(chan_id)
    del_channel_container(channel_4_id)
    del_channel_container(channel_6_id)
