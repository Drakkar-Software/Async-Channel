# Channel [2.0.0](https://github.com/Drakkar-Software/channel/blob/master/CHANGELOG.md)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d6bc3f05475c463189dbd509cfc94afe)](https://app.codacy.com/gh/Drakkar-Software/channel?utm_source=github.com&utm_medium=referral&utm_content=Drakkar-Software/channel&utm_campaign=Badge_Grade_Dashboard)
[![PyPI](https://img.shields.io/pypi/v/channel.svg)](https://pypi.python.org/pypi/channel/)
[![Build Status](https://api.travis-ci.com/Drakkar-Software/channel.svg?branch=master)](https://travis-ci.com/Drakkar-Software/channel) 
[![Build Status](https://dev.azure.com/drakkarsoftware/channel/_apis/build/status/Drakkar-Software.channel?branchName=master)](https://dev.azure.com/drakkarsoftware/channel/_build/latest?definitionId=3&branchName=master)
[![Build Status](https://cloud.drone.io/api/badges/Drakkar-Software/channel/status.svg)](https://cloud.drone.io/Drakkar-Software/channel)
[![Coverage Status](https://coveralls.io/repos/github/Drakkar-Software/channel/badge.svg?branch=master)](https://coveralls.io/github/Drakkar-Software/channel?branch=master)
[![Doc Status](https://readthedocs.org/projects/octobot-channels/badge/?version=stable)](https://octobot-channels.readthedocs.io/en/stable/?badge=stable)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[OctoBot](https://github.com/Drakkar-Software/OctoBot) channels package.

## Installation
With python3 : `pip install channel`

## Usage
Example
```python
import channel.consumer as consumer
import channel.producer as producer
import channel.channels as channels
import channel.util as util

class AwesomeProducer(producer.Producer):
    pass

class AwesomeConsumer(consumer.Consumer):
    pass

class AwesomeChannel(channels.Channel):
    PRODUCER_CLASS = AwesomeProducer
    CONSUMER_CLASS = AwesomeConsumer

async def callback(data):
    print("Consumer called !")
    print("Received : " + data)

# Creates the channel
await util.create_channel_instance(AwesomeChannel, channels.Channels)

# Add a new consumer to the channel
await channels.Channels.get_chan("Awesome").new_consumer(callback)

# Creates a producer that send data to the consumer through the channel
producer = AwesomeProducer(channels.Channels.get_chan("Awesome"))
await producer.run()
await producer.send("test")

# Stops the channel with all its producers and consumers
# await channels.Channels.get_chan("Awesome").stop()
```

# Developer documentation
On [readthedocs.io](https://octobot-channels.readthedocs.io/en/latest/)
