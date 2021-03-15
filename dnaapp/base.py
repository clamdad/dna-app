# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

import asyncio
import json

from atomdb.base import JSONModel
from atomdb.base import JSONSerializer


class Base(JSONModel):
    """ Base class for application objects

    This class is used as a model class that supports typed attributes,
    and conversion to/from and JSON objects
    """

    def __str__(self):
        kwargs = self.__getstate__()
        kwargs.pop('_id')
        kwargs.pop('__model__')
        kwargs.pop('__ref__')
        kwstr = ', '.join(f'{key}={value}' for key, value in kwargs.items())
        return '{}({})'.format(type(self).__name__, kwstr)


def from_json_state(state):
    """ Convert object state to an Model, dict, or list

    Parameters
    ----------
    state: dict
        Object state in JSON unserializable format

    Returns
    -------
    model: Base, dict, or list
        Object converted from JSON
    """

    decoder = JSONSerializer()

    async def decode_state(json_state):
        obj = await decoder.unflatten(json_state)
        return obj

    result = asyncio.run(decode_state(state))

    return result


def to_json_state(model, classinfo=True):
    """ Convert an object o JSON serializable state

    Parameters
    ----------
    model: Base, dict, or list
        Object to convet to json

    classinfo: bool
        Include class information (__model__, _id, __ref__)
        in serialized output

    Returns
    -------
    result: dict
        Object state in JSON format
    """
    encoder = JSONSerializer()

    state = encoder.flatten(model)

    if not classinfo:
        state.pop('_id')
        state.pop('__model__')
        state.pop('__ref__')

    return state


def to_json(model, classinfo=True):
    """ Convert model to JSON string

    Parameters
    ----------
    model: Base
        Model to convert to json string

    Returns
    -------
    str

    """
    state = to_json_state(model, classinfo)

    return json.dumps(state, indent=2)


def from_json(jstr, cls=None):
    """

    Parameters
    ----------
    jstr
    cls

    Returns
    -------

    """
    state = json.loads(jstr)
    obj = from_json_state(state)
    if cls:
        return cls(**obj)
    else:
        return obj
