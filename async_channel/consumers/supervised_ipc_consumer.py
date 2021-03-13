# pylint: disable=too-many-instance-attributes
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
Define async_channel SupervisedIPCConsumer class
"""

import async_channel.consumers.ipc_consumer as ipc_consumer


class SupervisedIPCConsumer(ipc_consumer.IPCConsumer):
    """
    A SupervisedIPCConsumer is an IPCConsumer that notifies a dedicated socket with its producer when its work is done
    """

    async def consume_ends(self) -> None:
        """
        The method called when the work is done
        """
        # TODO
