# cython: language_level=3
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

from octobot_commons.logging.logging_util import get_logger

from octobot_channels import CONSUMER_CALLBACK_TYPE
from octobot_channels.channels.channel_instances import ChannelInstances

"""
TODO
A Channel is 
"""


class Channel(object):
    # Channel producer class
    PRODUCER_CLASS = None

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

        # Channel subscribed producers list
        self.producers = []

        # Channel subscribed consumers dict
        self.consumers = {}

        # Used to perform global send from non-producer context
        self.internal_producer = None

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.replace('Channel', '')

    def new_consumer(self, callback: CONSUMER_CALLBACK_TYPE, size=0, **kwargs):
        """
        Create an appropriate consumer instance for this channel
        :param callback: method that should be called when consuming the queue
        :param size: queue size, default 0
        :return: a new consumer instance
        """
        raise NotImplemented("new consumer is not implemented")

    def register_producer(self, producer, **kwargs) -> None:
        """
        Add the producer to producers list
        Can be overwritten to perform additional action when registering
        :param Producer producer: created channel producer to register
        :param kwargs: additional arguments available for overwritten methods
        :return: None
        """
        self.producers.append(producer)

    def get_consumers(self, **kwargs) -> dict:
        """
        Should be overwritten according to the class needs
        :param kwargs:
        :return: the subscribed consumers dict
        """
        return self.consumers

    async def start(self) -> None:
        """
        Call each registered consumers start method
        :return: None
        """
        for consumer in [consumer.values() for consumer in self.consumers.values()]:
            await consumer.start()

    async def stop(self) -> None:
        """
        Call each registered consumers and producers stop method
        :return: None
        """
        for consumer in [consumer.values() for consumer in self.consumers.values()]:
            await consumer.stop()

        for producer in self.producers:
            await producer.stop()

    async def run(self) -> None:
        """
        Call each registered consumers run method
        :return: None
        """
        for consumer in [consumer.values() for consumer in self.consumers.values()]:
            await consumer.run()

    async def modify(self, **kwargs) -> None:
        """
        Call each registered producers modify method
        :return: None
        """
        for producer in self.producers:
            await producer.modify(**kwargs)

    def get_internal_producer(self, **kwargs) -> object:
        """
        Returns internal producer if exists else creates it
        :param kwargs: arguments for internal producer __init__
        :return: internal producer instance
        """
        if not self.internal_producer:
            self.internal_producer = self.PRODUCER_CLASS(self, **kwargs)
        return self.internal_producer


class Channels:
    @staticmethod
    def set_chan(chan: Channel, name: str) -> None:
        """
        Set a new Channel instance in the channels list according to channel name
        :param chan: new Channel instance
        :param name: name of the channel
        :return: None
        """
        chan_name = chan.get_name() if name else name
        if chan_name not in ChannelInstances.instance().channels:
            ChannelInstances.instance().channels[chan_name] = chan
        else:
            raise ValueError(f"Channel {chan_name} already exists.")

    @staticmethod
    def get_chan(chan_name: str, **kwargs) -> Channel:
        """
        Return the channel instance from channel name
        :param chan_name: the channel name
        :param kwargs:
        :return: the Channel instance
        """
        return ChannelInstances.instance().channels[chan_name]
