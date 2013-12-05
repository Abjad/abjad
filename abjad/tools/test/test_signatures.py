# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import durationtools
from abjad.tools import mathtools


# only immutable types are allowed;
# lists and other mutables are not allowed as initializer keyword values
valid_types = (
    bool,
    float,
    int,
    str,
    tuple,
    type(None),
    datastructuretools.OrdinalConstant,
    durationtools.Duration,
    mathtools.Infinity,
    mathtools.NegativeInfinity,
    )


classes = documentationtools.list_all_abjad_classes()
@pytest.mark.parametrize('obj', classes)
def test_signatures_01(obj):
    r'''Make sure class initializer keyword argument values are immutable.
    '''

    for attr in inspect.classify_class_attrs(obj):
        if attr.defining_class is not obj:
            continue
        elif attr.kind != 'method':
            continue
        argument_specification = inspect.getargspec(attr.object)
        keyword_argument_names = argument_specification.args[1:]
        keyword_argument_values = argument_specification.defaults
        if keyword_argument_values is None:
            continue
        for name, value in zip(
            keyword_argument_names, keyword_argument_values):
            assert isinstance(value, valid_types), (attr.name, name, value)
            if isinstance(value, tuple):
                assert all(isinstance(x, valid_types) for x in value)


functions = documentationtools.list_all_abjad_functions()
@pytest.mark.parametrize('obj', functions)
def test_signatures_02(obj):
    r'''Make sure function keyword argument values are immutable.
    '''

    argument_specification = inspect.getargspec(obj)
    keyword_argument_names = argument_specification.args[1:]
    keyword_argument_values = argument_specification.defaults
    if keyword_argument_values is None:
        return
    for name, value in zip(
        keyword_argument_names, keyword_argument_values):
        assert isinstance(value, valid_types), (name, value)
        if isinstance(value, tuple):
            assert all(isinstance(x, valid_types) for x in value)
