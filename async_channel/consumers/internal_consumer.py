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
Define async_channel InternalConsumer class
"""

import async_channel.consumers.consumer as consumer


class InternalConsumer(consumer.Consumer):
    """
    An InternalConsumer is a classic Consumer except that his callback is declared internally
    """

    def __init__(self, channel):
        """
        The constructor only override the callback to be the 'internal_callback' method
        """
        super().__init__(channel, None)
        self.callback = self.internal_callback

    async def internal_callback(self, **kwargs: dict) -> None:
        """
        The method triggered when the producer has pushed into the channel
        :param kwargs: Additional params
        """
        raise NotImplementedError("internal_callback is not implemented")
