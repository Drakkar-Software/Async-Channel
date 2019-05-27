from octobot_channels.channels import RECENT_TRADES_CHANNEL
from octobot_channels.channels.exchange.exchange_channel import ExchangeChannels


def test_get_chan():
    ExchangeChannels.get_chan(RECENT_TRADES_CHANNEL, "")
