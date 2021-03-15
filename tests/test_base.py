# ------------------------------------------------------------------------------
# Copyright (c) 2021, Mike Babst
#
# Distributed under the terms of the MIT License
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
from atom.api import Int, Str

from dnaapp.base import Base, to_json_state, from_json_state, to_json, from_json


class BaseSubclass(Base):
    name = Str()
    amount = Int()


def test_class_state():
    obj = BaseSubclass(amount=5)
    state = obj.__getstate__()


def test_encode_model():
    """ Test encoding a model to JSON

    """

    obj = BaseSubclass(amount=5, name='Aloysius')
    state = to_json_state(obj)
    assert state['__model__'] == 'tests.test_base.BaseSubclass'
    assert state['name'] == 'Aloysius'


def test_decode_model():
    """ Test restoring model and other objects from JSON state

    """

    state = {'__model__': 'tests.test_base.BaseSubclass', '__ref__': '9230a086921eae1f94b6fcdb1940cc', '_id': '',
             'name': 'frank', 'amount': 5}
    obj = from_json_state(state)

    state = {'__model__': 'tests.test_base.BaseSubclass', 'name': 'Bartholemew', 'amount': 5}
    obj = from_json_state(state)
    assert isinstance(obj, BaseSubclass)
    assert obj.amount == 5
    assert obj.name == 'Bartholemew'

    state = {'name': 'Aloysius', 'amount': 5}
    obj = from_json_state(state)
    assert isinstance(obj, dict)
    assert obj['amount'] == 5
    assert obj['name'] == 'Aloysius'


def test_to_from_json():
    obj = BaseSubclass(amount=5, name='Aloysius')
    jstr2 = to_json(obj)
    obj2 = from_json(jstr2)
    assert obj2 is not obj
    assert isinstance(obj2, BaseSubclass)
    assert obj2.amount == 5

def test_to_from_json_noclass():
    obj = BaseSubclass(amount=5, name='Aloysius')
    jstr2 = to_json(obj, classinfo=False)
    obj2 = from_json(jstr2, BaseSubclass)
    assert obj2 is not obj
    assert isinstance(obj2, BaseSubclass)
    assert obj2.amount == 5

def test_base_str():
    obj = BaseSubclass(amount=5, name='Aloysius')
    ostr = str(obj)
    assert ostr == 'BaseSubclass(name=Aloysius, amount=5)'