# pylint: disable=E0611
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
from octobot_commons.logging.logging_util import get_logger
from octobot_commons.singleton.singleton_class import Singleton


class ChannelInstances(Singleton):
    """
    Singleton that contains Channel instances
    """

    def __init__(self):
        self.channels = {}


def set_chan_at_id(chan, name) -> None:
    """
    Add a new channel to the channels instances dictionary at chan.id
    :param chan: the channel instance
    :param name: the channel name
    """
    chan_name = chan.get_name() if name else name

    try:
        chan_instance = ChannelInstances.instance().channels[chan.chan_id]
    except KeyError:
        ChannelInstances.instance().channels[chan.chan_id] = {}
        chan_instance = ChannelInstances.instance().channels[chan.chan_id]

    if chan_name not in chan_instance:
        chan_instance[chan_name] = chan
        return chan
    raise ValueError(f"Channel {chan_name} already exists.")


def get_channels(chan_id) -> dict:
    """
    Get channel instances by channel id
    :param chan_id: the channel id
    :return: the channel instances at channel id
    """
    try:
        return ChannelInstances.instance().channels[chan_id]
    except KeyError:
        raise KeyError(f"Channels not found with chan_id: {chan_id}")


def del_channel_container(chan_id) -> None:
    """
    Delete all channel id instances
    :param chan_id: the channel id
    """
    ChannelInstances.instance().channels.pop(chan_id, None)


def get_chan_at_id(chan_name, chan_id) -> object:
    """
    Get the channel instance that matches the name and the id
    :param chan_name: the channel name
    :param chan_id: the channel id
    :return: the channel instance if any
    """
    try:
        return ChannelInstances.instance().channels[chan_id][chan_name]
    except KeyError:
        raise KeyError(f"Channel {chan_name} not found with chan_id: {chan_id}")


def del_chan_at_id(chan_name, chan_id) -> None:
    """
    Delete the channel instance that matches the name and the id
    :param chan_name: the channel name
    :param chan_id: the channel id
    """
    try:
        ChannelInstances.instance().channels[chan_id].pop(chan_name, None)
    except KeyError:
        get_logger(ChannelInstances.__name__).warning(
            f"Can't del chan {chan_name} with chan_id: {chan_id}"
        )
