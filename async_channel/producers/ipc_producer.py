#  Drakkar-Software Async-Channel
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
"""
Define async_channel IPCProducer class
"""
import asyncio
import json

import zmq
import zmq.asyncio

import async_channel.producers.producer as producer


class IPCProducer(producer.Producer):
    """
    An IPCProducer has the same behaviour than a class Producer except that it send produced data into
    the channel socket instead of a consumer queue
    """

    # seconds to wait to fix slow subscriber problem
    SLOW_SUBSCRIBER_FIX_TIME = 4

    def __init__(self, channel):
        super().__init__(channel)

        # the Channel ipc socket
        self.ipc_socket = None

        # connect to the channel ipc socket
        self._ipc_connect()

    async def run(self) -> None:
        """
        Synchronize consumers by sending a "hello" payload
        Inspired from slow subscriber detection pattern
        https://zguide.zeromq.org/docs/chapter5/#Slow-Subscriber-Detection-Suicidal-Snail-Pattern
        """
        await super().run()
        await asyncio.sleep(self.SLOW_SUBSCRIBER_FIX_TIME)
        await self.send({})

    async def send(self, data, consumers=None) -> None:
        """
        Send to each consumer data though the ipc socket
        """
        if consumers is not None:
            self.logger.warning("Consumer filtering is not available with IPCProducer")
        await self.ipc_socket.send_multipart([json.dumps(data).encode("utf-8")])

    # pylint: disable=no-member
    def _ipc_connect(self):
        """
        Connect to Channel socket when IPC is enabled for this channel
        """
        ipc_context = zmq.asyncio.Context.instance()
        self.ipc_socket = ipc_context.socket(zmq.PUB)
        self.ipc_socket.bind(self.channel.ipc_url)

    async def stop(self) -> None:
        """
        Close IPC socket
        """
        await super().stop()
        self.ipc_socket.close()
        self.ipc_socket = None
