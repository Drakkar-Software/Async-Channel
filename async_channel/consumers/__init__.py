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
Define Consumers implementation and usage
"""
from async_channel.consumers import consumer
from async_channel.consumers.consumer import Consumer

from async_channel.consumers import ipc_consumer
from async_channel.consumers.ipc_consumer import IPCConsumer

from async_channel.consumers import internal_consumer
from async_channel.consumers.internal_consumer import InternalConsumer

from async_channel.consumers import supervised_consumer
from async_channel.consumers.supervised_consumer import SupervisedConsumer

from async_channel.consumers import supervised_ipc_consumer
from async_channel.consumers.supervised_ipc_consumer import SupervisedIPCConsumer

__all__ = [
    "Consumer",
    "IPCConsumer",
    "InternalConsumer",
    "SupervisedConsumer",
    "SupervisedIPCConsumer",
]
