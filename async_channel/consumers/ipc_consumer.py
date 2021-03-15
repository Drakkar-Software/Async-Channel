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
Define async_channel IPCConsumer class
"""
import json

import zmq
import zmq.asyncio

import async_channel
import async_channel.consumers.consumer as consumer


class IPCConsumer(consumer.Consumer):
    """
    An IPCConsumer is a Consumer that connect to Channel ipc socket instead of using a queue
    """

    def __init__(
        self,
        channel,
        callback: object,
        size: int = async_channel.constants.DEFAULT_QUEUE_SIZE,
        priority_level: int = async_channel.enums.ChannelConsumerPriorityLevels.HIGH.value,
    ):
        super().__init__(
            channel=channel, callback=callback, size=size, priority_level=priority_level
        )

        # the Channel ipc socket
        self.ipc_socket = None

        self._ipc_connect()

    async def receive(self):
        """
        Wait and receive data from the ipc socket
        :return: the received data
        """
        return json.loads((await self.ipc_socket.recv_multipart())[0])

    # pylint: disable=no-member
    def _ipc_connect(self):
        """
        Connect to Channel socket, set self.ipc_socket value with the socket that was created
        and subscribed to Channel name subject
        """
        ipc_context = zmq.asyncio.Context.instance()
        self.ipc_socket = ipc_context.socket(zmq.SUB)
        self.ipc_socket.connect(self.channel.ipc_url)
        self.ipc_socket.setsockopt_string(zmq.SUBSCRIBE, "")

    async def stop(self) -> None:
        """
        Close IPC socket
        """
        await super().stop()
        self.ipc_socket.close()
        self.ipc_socket = None
