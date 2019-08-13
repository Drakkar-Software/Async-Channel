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

cdef class Consumer:
    cdef public object logger          # object type = Logger
    cdef public object queue    # object type = asyncio.Queue
    cdef public object callback        # object type = CONSUMER_CALLBACK_TYPE
    cdef public object consume_task    # object type = asyncio.Task

    cdef public bint should_stop
    cdef public bint filter_size

    cpdef void create_task(self)
