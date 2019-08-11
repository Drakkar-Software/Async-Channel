# OctoBot-Channels [1.1.1](https://github.com/Drakkar-Software/OctoBot-Channels/blob/master/CHANGELOG.md)
[![PyPI](https://img.shields.io/pypi/v/OctoBot-Channels.svg)](https://pypi.python.org/pypi/OctoBot-Channels/)
[![Build Status](https://api.travis-ci.com/Drakkar-Software/OctoBot-Channels.svg?branch=master)](https://travis-ci.org/Drakkar-Software/OctoBot-Channels) 
[![Build status](https://ci.appveyor.com/api/projects/status/erg9ebvtco73x5h4?svg=true)](https://ci.appveyor.com/project/Herklos/octobot-channels)

OctoBot channels package.

## Installation
With python3 : `pip install OctoBot-Channels`

## Usage
Example
```
from octobot_channels import Consumer, Producer
from octobot_channels.channels import Channels, Channel
from octobot_channels.util import create_channel_instance

class AwesomeProducer(Producer):
    pass

class AwesomeConsumer(Consumer):
    pass

class AwesomeChannel(Channel):
    PRODUCER_CLASS = MyAwesomeProducer
    CONSUMER_CLASS = MyAwesomeConsumer

async def callback(data):
    print("Consumer called !")
    print("Received : " + data)

# Creates the channel
await create_channel_instance(MyChannel, Channels)

# Add a new consumer to the channel
await Channels.get_chan("Awesome").new_consumer(callback)

# Creates a producer that send data to the consumer through the channel
producer = TestProducer(Channels.get_chan("Awesome"))
await producer.send("test")

# Stops the channel with all its producers and consumers
# await Channels.get_chan("Awesome").stop()
```
