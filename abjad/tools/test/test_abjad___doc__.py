# -*- encoding: utf-8 -*-
import inspect
import pytest
from abjad import *


ignored_names = (
    '__dict__',
    '__init__',
    '__new__',
    '__weakref__',
    'context_name',
    'denominator',
    'duration',
    'multiplier',
    'music',
    'numerator',
    'optional_id',
    'optional_context_mod',
    'push_signature',
    'type',
    'value',
    )

ignored_classes = (
    datastructuretools.Enumeration,
    lilypondparsertools.LilyPondLexicalDefinition,
    lilypondparsertools.LilyPondSyntacticalDefinition,
    lilypondparsertools.ReducedLyParser,
    lilypondparsertools.SchemeParser,
    rhythmtreetools.RhythmTreeParser,
    )


classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )
@pytest.mark.parametrize('obj', classes)
def test_abjad___doc___01(obj):
    r'''All classes have a docstring. All class methods have a docstring.
    '''

    assert obj.__doc__ is not None
    for attr in inspect.classify_class_attrs(obj):
        if attr.name in ignored_names:
            continue
        elif attr.defining_class is not obj:
            continue
        if attr.name[0].isalpha() or attr.name.startswith('__'):
            message = '{}.{}'
            message = message.format(obj.__name__, attr.name)
            assert getattr(obj, attr.name).__doc__ is not None, message


functions = documentationtools.list_all_abjad_functions()
@pytest.mark.parametrize('obj', functions)
def test_abjad___doc___02(obj):
    r'''All functions have a docstring.
    '''

    assert obj.__doc__ is not None