# cython: language_level=3, boundscheck=False, wraparound=False
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
from octobot_commons.singleton.singleton_class cimport Singleton

from octobot_channels.channels.channel cimport Channel

cdef class ChannelInstances(Singleton):
    cdef public dict channels

cpdef Channel get_chan_at_id(str chan_name, str chan_id)
cpdef dict get_channels(str chan_id)
cpdef Channel set_chan_at_id(Channel chan, str name)
cpdef void del_channel_container(str chan_id)
cpdef void del_chan_at_id(str name, str chan_id)
