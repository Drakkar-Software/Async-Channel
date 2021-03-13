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
import zmq

import async_channel.producers.producer as producer


class IPCProducer(producer.Producer):
    """
    An IPCProducer has the same behaviour than a class Producer except that it send produced data into
    the channel socket instead of a consumer queue
    """

    def __init__(self, channel):
        super().__init__(channel)

        # the Channel ipc socket
        self.ipc_socket = None

        # connect to the channel ipc socket
        self._ipc_connect()

    async def send(self, data) -> None:
        pass  # TODO

    async def push(self, **kwargs) -> None:
        """
        Push notification that new data should be sent implementation
        When nothing should be done on data : self.send()
        """

    # pylint: disable=no-member
    def _ipc_connect(self):
        """
        Connect to Channel socket when IPC is enabled for this channel
        """
        ipc_context = zmq.Context.instance()
        self.ipc_socket = ipc_context.socket(zmq.PUB)
        self.ipc_socket.bind(self.channel.ipc_url)
