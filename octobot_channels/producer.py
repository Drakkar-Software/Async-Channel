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
import asyncio

from octobot_commons.logging.logging_util import get_logger

"""
A channel Producer
"""


class Producer:
    def __init__(self, channel):
        self.logger = get_logger(self.__class__.__name__)

        # Related channel instance
        self.channel = channel

        """
        Should only be used with .cancel()
        """
        self.produce_task = None

        """
        Should be used as the perform while loop condition
            while(self.should_stop):
                ...
        """
        self.should_stop = False

    async def send(self, data, **kwargs):
        """
        Send to each consumer data though its queue
        :param data: data to be put into consumers queues
        :param kwargs:
        :return: None
        """
        """
        The implementation should use 'self.channel.get_consumers'
        Example
            for consumer in self.channel.get_consumers():
                await consumer.queue.put({
                    "my_key": my_key_value
                })
        """
        for consumer in self.channel.get_consumers():
            consumer.queue.put(data)

    async def push(self, **kwargs):
        """
        Push notification that new data should be sent implementation
        When nothing should be done on data : self.send()
        :return: None
        """
        pass

    async def start(self):
        """
        Should be implemented for producer's non-triggered tasks
        :return: None
        """
        pass

    async def perform(self, **kwargs):
        """
        Should implement producer's non-triggered tasks
        Can be use to force producer to perform tasks
        :return: None
        """
        pass

    async def modify(self, **kwargs):
        """
        Should be implemented when producer can be modified during perform()
        :return: None
        """
        pass

    async def stop(self):
        """
        Stops non-triggered tasks management
        :return: None
        """
        self.should_stop = True
        if self.produce_task:
            self.produce_task.cancel()

    def create_task(self):
        """
        Creates a new asyncio task that contains start() execution
        :return: None
        """
        self.produce_task = asyncio.create_task(self.start())

    async def run(self):
        """
        Start the producer main task
        :return: None
        """
        self.channel.register_producer(self)
        self.create_task()
