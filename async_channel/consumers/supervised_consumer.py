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
Define async_channel SupervisedConsumer class
"""

import async_channel.consumers.consumer as consumer


class SupervisedConsumer(consumer.Consumer):
    """
    A SupervisedConsumer is a classic Consumer that notifies the queue when its work is done
    """

    async def consume_ends(self) -> None:
        """
        The method called when the work is done
        """
        try:
            self.queue.task_done()
        except ValueError:  # when task_done() is called when the Exception was CancelledError
            pass
