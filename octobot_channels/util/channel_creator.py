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


async def create_all_subclasses_channel(channel_class, channels_class, **kwargs):
    for to_be_created_channel_class in channel_class.__subclasses__():
        created_channel = to_be_created_channel_class(**kwargs)
        channels_class.set_chan(created_channel, name=to_be_created_channel_class.get_name())
        await created_channel.start()
