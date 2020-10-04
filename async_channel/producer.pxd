# cython: language_level=3, boundscheck=False, wraparound=False
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

cdef class Producer:
    cdef public object channel # object type = Channel
    cdef public object logger  # object type = logger
    cdef public object produce_task  # object type = asyncio.Task

    cdef public bint should_stop
    cdef public bint is_running

    cpdef void create_task(self)
    cpdef bint is_consumers_queue_empty(self, int priority_level)
