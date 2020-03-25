# cython: language_level=3, wraparound=False
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
from octobot_channels.producer cimport Producer

cdef class Channel(object):
    cdef object logger

    cdef public list producers
    cdef public list consumers

    cdef public Producer internal_producer

    cdef public bint is_paused

    cpdef void add_new_consumer(self, object consumer, dict consumer_filters)
    cpdef list get_consumers(self)
    cpdef object get_producers(self)
    cpdef void unregister_producer(self, Producer producer)
    cpdef list get_consumer_from_filters(self, dict consumer_filters)
    cpdef void flush(self)

    cdef list _filter_consumers(self, dict consumer_filters)

cpdef Channel set_chan(Channel chan, str name)
cpdef void del_chan(str name)
cpdef Channel get_chan(str chan_name)

cdef bint _check_filters(dict consumer_filters, dict expected_filters)
