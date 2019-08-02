import pytest

from octobot_channels.channels.channel import Channels, Channel

TEST_CHANNEL = "Test"


class TestChannel(Channel):
    pass


async def _create_channels():
    for channel_class in Channel.__subclasses__():
        channel = channel_class()
        Channels.set_chan(channel, name=channel_class.get_name())
        await channel.start()


@pytest.mark.asyncio
async def test_get_chan():
    await _create_channels()
    Channels.get_chan(TEST_CHANNEL)
