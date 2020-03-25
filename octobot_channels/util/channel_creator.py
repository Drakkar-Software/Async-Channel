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
from typing import ClassVar, Callable

from octobot_channels.channels.channel import Channel


async def create_all_subclasses_channel(
    channel_class: ClassVar, set_chan_method: Callable, **kwargs: dict
) -> None:
    """
    Calls 'channel_creator.create_channel_instance' for each subclasses of the 'channel_class' param
    :param channel_class: The class in which to search for subclasses
    :param set_chan_method: The method reference used in 'channel_creator.create_channel_instance'
    :param kwargs: Some additional params passed to 'channel_creator.create_channel_instance'
    """
    for to_be_created_channel_class in channel_class.__subclasses__():
        await create_channel_instance(
            to_be_created_channel_class, set_chan_method, **kwargs
        )


async def create_channel_instance(
    channel_class: ClassVar, set_chan_method: Callable, **kwargs: dict
) -> Channel:
    """
    Creates, initialize and start a channel instance
    :param channel_class: The class to instantiate with optional kwargs params
    :param set_chan_method: The method to call to add the created channel instance to a Channel list
    :param kwargs: Some additional params passed to the 'channel_class' constructor
    :return: the created 'channel_class' instance
    """
    created_channel = channel_class(**kwargs)
    set_chan_method(created_channel, name=channel_class.get_name())
    await created_channel.start()
    return created_channel
