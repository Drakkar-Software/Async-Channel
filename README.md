# OctoBot-Channels [1.4.3](https://github.com/Drakkar-Software/OctoBot-Channels/blob/master/CHANGELOG.md)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d6bc3f05475c463189dbd509cfc94afe)](https://app.codacy.com/gh/Drakkar-Software/OctoBot-Channels?utm_source=github.com&utm_medium=referral&utm_content=Drakkar-Software/OctoBot-Channels&utm_campaign=Badge_Grade_Dashboard)
[![PyPI](https://img.shields.io/pypi/v/OctoBot-Channels.svg)](https://pypi.python.org/pypi/OctoBot-Channels/)
[![Build Status](https://api.travis-ci.com/Drakkar-Software/OctoBot-Channels.svg?branch=master)](https://travis-ci.com/Drakkar-Software/OctoBot-Channels) 
[![Build Status](https://dev.azure.com/drakkarsoftware/OctoBot-Channels/_apis/build/status/Drakkar-Software.OctoBot-Channels?branchName=master)](https://dev.azure.com/drakkarsoftware/OctoBot-Channels/_build/latest?definitionId=3&branchName=master)
[![Build Status](https://cloud.drone.io/api/badges/Drakkar-Software/OctoBot-Channels/status.svg)](https://cloud.drone.io/Drakkar-Software/OctoBot-Channels)
[![Coverage Status](https://coveralls.io/repos/github/Drakkar-Software/OctoBot-Channels/badge.svg?branch=master)](https://coveralls.io/github/Drakkar-Software/OctoBot-Channels?branch=master)
[![Doc Status](https://readthedocs.org/projects/octobot-channels/badge/?version=stable)](https://octobot-channels.readthedocs.io/en/stable/?badge=stable)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[OctoBot](https://github.com/Drakkar-Software/OctoBot) channels package.

## Installation
With python3 : `pip install OctoBot-Channels`

## Usage
Example
```python
from octobot_channels.consumer import Consumer
from octobot_channels.producer import Producer
from octobot_channels.channels.channel import Channel
from octobot_channels.channels.channel_instances import Channels
from octobot_channels.util.channel_creator import create_channel_instance

class AwesomeProducer(Producer):
    pass

class AwesomeConsumer(Consumer):
    pass

class AwesomeChannel(Channel):
    PRODUCER_CLASS = AwesomeProducer
    CONSUMER_CLASS = AwesomeConsumer

async def callback(data):
    print("Consumer called !")
    print("Received : " + data)

# Creates the channel
await create_channel_instance(AwesomeChannel, Channels)

# Add a new consumer to the channel
await Channels.get_chan("Awesome").new_consumer(callback)

# Creates a producer that send data to the consumer through the channel
producer = AwesomeProducer(Channels.get_chan("Awesome"))
await producer.run()
await producer.send("test")

# Stops the channel with all its producers and consumers
# await Channels.get_chan("Awesome").stop()
```

# Developer documentation
On [readthedocs.io](https://octobot-channels.readthedocs.io/en/latest/)
