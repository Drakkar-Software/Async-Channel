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


class Producer:
    """
    A Producers are responsible for producing some output that may be placed onto the head of a queue.
    A Consumer will consume this data through the same shared queue.
    A producer doesn't need to know or care about its consumers.
    But if there is no space in the queue, it won't be able to share what it has produced.
    """

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

        """
        Should be used to know if the producer is already started
        """
        self.is_running = False

    async def send(self, data) -> None:
        """
        Send to each consumer data though its queue
        :param data: data to be put into consumers queues

        The implementation should use 'self.channel.get_consumers'
        Example
            >>> for consumer in self.channel.get_consumers():
                    await consumer.queue.put({
                        "my_key": my_key_value
                    })
        """
        for consumer in self.channel.get_consumers():
            await consumer.queue.put(data)

    async def push(self, **kwargs) -> None:
        """
        Push notification that new data should be sent implementation
        When nothing should be done on data : self.send()
        """

    async def start(self) -> None:
        """
        Should be implemented for producer's non-triggered tasks
        """

    async def pause(self) -> None:
        """
        Called when the channel runs out of consumer
        """

    async def resume(self) -> None:
        """
        Called when the channel is no longer out of consumer
        """

    async def perform(self, **kwargs) -> None:
        """
        Should implement producer's non-triggered tasks
        Can be use to force producer to perform tasks
        """

    async def modify(self, **kwargs) -> None:
        """
        Should be implemented when producer can be modified during perform()
        """

    async def wait_for_processing(self) -> None:
        """
        Should be used only with SupervisedConsumers
        It will wait until all consumers have notified that their consume() method have ended
        """
        await asyncio.gather(
            *[consumer.queue.join() for consumer in self.channel.get_consumers()]
        )

    async def stop(self) -> None:
        """
        Stops non-triggered tasks management
        """
        self.should_stop = True
        self.is_running = False
        if self.produce_task:
            self.produce_task.cancel()

    def create_task(self) -> None:
        """
        Creates a new asyncio task that contains start() execution
        """
        self.is_running = True
        self.produce_task = asyncio.create_task(self.start())

    async def run(self) -> None:
        """
        Start the producer main task
        Should call 'self.channel.register_producer'
        """
        await self.channel.register_producer(self)
        self.create_task()
