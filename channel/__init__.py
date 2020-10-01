#  Drakkar-Software channel
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
Define channel project
"""

from channel import constants
from channel.constants import (
    CHANNEL_WILDCARD,
    DEFAULT_QUEUE_SIZE,
)

from channel import enums
from channel.enums import ChannelConsumerPriorityLevels

from channel import producer
from channel.producer import Producer

from channel import consumer
from channel.consumer import (
    Consumer,
    InternalConsumer,
    SupervisedConsumer,
)

PROJECT_NAME = "channel"
VERSION = "2.0.0"  # major.minor.revision

__all__ = [
    "CHANNEL_WILDCARD",
    "DEFAULT_QUEUE_SIZE",
    "ChannelConsumerPriorityLevels",
    "Producer",
    "Consumer",
    "InternalConsumer",
    "SupervisedConsumer",
    "PROJECT_NAME",
    "VERSION",
]
