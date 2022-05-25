import os, sys
import pathlib
import asyncio
from asyncio import Queue
from dataclasses import dataclass, field, InitVar
import typing as t
from typing import Dict, ClassVar


"""
# Possible Project Expression

Switchboard - A Queue Router: instantiable objects from a service description for async Python applications (framework agnostic)

- only consumers:
    - require different handlers on condition of the incoming message, or the in_force subscription of a queue task, so multi- subscriptions and subscription conditionals
- only producers:
    - have multiple subscribers
    - multiple conditions on tasks prior to send;
        - filtering requirement with respect to subscribers
    
One Goal:
    - to provide an application multiple configurable, parallel running queue tasks on both consumer and producer sides which optimally route messages according to a switchboard methodology, comprising a mini, in-app communications API, or less grandiose, instantiable popup queues with handler routing tables and pre-flight conditionals

"""

channels = {} # TODO: complete the QChannels class and helpers


@dataclass
class QChannels:

    queue_channels = {}
    list_of_queues_reqd = []
    engage_swarm: InitVar

    def __post_init__(self):
        if engage_swarm:
            swarm_channels = swarm_channels()
            cls.queue_channels.update(swarm_channels)


async def get_swarm_queues():
    pass
    async def get_swarm_queue(): ...


async def queue_channels(qname):
    # a dict of all queues beneath channel designation
    channels['multiprocess'] = asyncio.Queue()
    # channels['swarm'] = await get_swarm_queues() # lookup by symbol,
    # # is receiving channel, any additional listeners require a 'splitter', routing from the consumer task -- eval may come in handy here, but let's find out
    # channels['analysis'] = await get_analysis_queues()
    # channels['ohlc'] = await get_ohlc_queues()
    return channels.get(qname, asyncio.Queue())


async def subscribe_to_queue_channel(): ...

async def get_queue_subscriber(): ...

async def get_queue_map(): 
    pass
    async def get_XtoZ_queue():
        # provision a queue like any other
        return asyncio.Queue()