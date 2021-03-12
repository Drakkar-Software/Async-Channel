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
Define async_channel global constants
"""
CHANNEL_WILDCARD = "*"

DEFAULT_QUEUE_SIZE = 0  # unlimited

# IPC constants
DEFAULT_IPC_PROTOCOL = "tcp"
DEFAULT_IPC_IP = "127.0.0.1"
DEFAULT_IPC_PORT = "5555"
DEFAULT_IPC_URL = f"{DEFAULT_IPC_PROTOCOL}://{DEFAULT_IPC_IP}:{DEFAULT_IPC_PORT}"
