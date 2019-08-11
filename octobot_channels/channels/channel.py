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
from typing import Iterable

from octobot_commons.logging.logging_util import get_logger

from octobot_channels import CONSUMER_CALLBACK_TYPE
from octobot_channels.channels.channel_instances import ChannelInstances

"""
A Channel is the object to connect a producer / producers class(es) to a consumer / consumers class(es)
It contains a registered consumers dict to notify every consumer when a producer 'send' something.
It contains a registered producers list to allow producer modification through 'modify'.
To access to channels a 'Channels' singleton is created to manage instances. 
"""


class Channel(object):
    # Channel producer class
    PRODUCER_CLASS = None

    # Channel consumer class
    CONSUMER_CLASS = None

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

    async def new_consumer(self, callback: CONSUMER_CALLBACK_TYPE, size=0, **kwargs) -> None:
        """
        Create an appropriate consumer instance for this channel and add it to the consumer list
        :param callback: method that should be called when consuming the queue
        :param size: queue size, default 0
        :return: None
        """
        await self.__add_new_consumer_and_run(self.CONSUMER_CLASS(callback))

    async def __add_new_consumer_and_run(self, consumer: CONSUMER_CLASS, **kwargs) -> None:
        """
        Should be called by 'new_consumer' to add the consumer to self.consumers and call 'consumer.run()'
        :param consumer: the consumer to add
        :param kwargs: additional params for consumer list
        :return: None
        """
        """
        The implementation should add the consumer to self.consumers and call consumer run() method
        Example
            self.consumers["consumer_key_id"] = [consumer]
            consumer.run()
        """
        Channel.init_consumer_if_necessary(self.consumers, self.CONSUMER_CLASS.__name__)
        self.consumers[self.CONSUMER_CLASS.__name__].append(consumer)
        await consumer.run()

    @staticmethod
    def init_consumer_if_necessary(consumer_list: Iterable, key: str, is_dict: bool = False) -> None:
        """
        Should be called by '__add_new_consumer_and_run' to create the consumer list
        :param consumer_list: current consumer list
        :param key: key to add if not exists
        :param is_dict: instantiates with a dict if True else list
        :return: None
        """
        if key not in consumer_list:
            consumer_list[key] = [] if not is_dict else {}

    def register_producer(self, producer, **kwargs) -> None:
        """
        Add the producer to producers list
        Can be overwritten to perform additional action when registering
        :param Producer producer: created channel producer to register
        :param kwargs: additional arguments available for overwritten methods
        :return: None
        """
        self.producers.append(producer)

    def get_consumers(self, **kwargs) -> Iterable:
        """
        Should be overwritten according to the class needs
        :param kwargs: consumers list filter params
        :return: the subscribed consumers dict
        """
        return [consumer for consumers in self.consumers.values() for consumer in consumers]

    async def start(self) -> None:
        """
        Call each registered consumers start method
        :return: None
        """
        for consumer in self.get_consumers():
            await consumer.start()

    async def stop(self) -> None:
        """
        Call each registered consumers and producers stop method
        :return: None
        """
        for consumer in self.get_consumers():
            await consumer.stop()

        for producer in self.producers:
            await producer.stop()

    async def run(self) -> None:
        """
        Call each registered consumers run method
        :return: None
        """
        for consumer in self.get_consumers():
            await consumer.run()

    async def modify(self, **kwargs) -> None:
        """
        Call each registered producers modify method
        :return: None
        """
        for producer in self.producers:
            await producer.modify(**kwargs)

    def get_internal_producer(self, **kwargs) -> PRODUCER_CLASS:
        """
        Returns internal producer if exists else creates it
        :param kwargs: arguments for internal producer __init__
        :return: internal producer instance
        """
        if not self.internal_producer:
            try:
                self.internal_producer = self.PRODUCER_CLASS(self, **kwargs)
            except TypeError:
                self.logger.exception("PRODUCER_CLASS not defined")
        return self.internal_producer


class Channels:
    @staticmethod
    def set_chan(chan, name) -> None:
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
    def del_chan(name) -> None:
        """
        Delete a Channel instance from the channels list according to channel name
        :param name: name of the channel to delete
        :return: None
        """
        if name in ChannelInstances.instance().channels:
            ChannelInstances.instance().channels.pop(name, None)

    @staticmethod
    def get_chan(chan_name: str, **kwargs) -> Channel:
        """
        Return the channel instance from channel name
        :param chan_name: the channel name
        :param kwargs:
        :return: the Channel instance
        """
        return ChannelInstances.instance().channels[chan_name]
