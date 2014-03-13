# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import documentationtools


classes = documentationtools.list_all_scoremanager_classes()
@pytest.mark.parametrize('obj', classes)
def test___doc___01(obj):
    r'''All classes have a docstring. All class methods have a docstring.
    '''

    ignored_names = (
        '__dict__',
        '__init__',
        )

    ignored_classes = (
        )

    assert obj.__doc__ is not None
    if obj.__name__ in ignored_classes:
        return
    for attr in inspect.classify_class_attrs(obj):
        if attr.name in ignored_names:
            continue
        elif attr.defining_class is not obj:
            continue
        if attr.name[0].isalpha() or attr.name.startswith('__'):
            message = '{}.{}'
            message = message.format(obj.__name__, attr.name)
            assert getattr(obj, attr.name).__doc__ is not None, message
