# -*- coding: utf-8 -*-
import inspect
import pytest
from abjad.tools import abjadbooktools
from abjad.tools import datastructuretools
from abjad.tools import documentationtools
from abjad.tools import lilypondparsertools
from abjad.tools import rhythmtreetools
from abjad.tools import systemtools


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
    abjadbooktools.CodeBlock,
    abjadbooktools.LaTeXDocumentHandler,
    abjadbooktools.SphinxDocumentHandler,
    datastructuretools.Enumeration,
    lilypondparsertools.LilyPondLexicalDefinition,
    lilypondparsertools.LilyPondSyntacticalDefinition,
    lilypondparsertools.ReducedLyParser,
    lilypondparsertools.SchemeParser,
    rhythmtreetools.RhythmTreeParser,
    systemtools.StorageFormatAgent,
    systemtools.FormatSpecification,
    systemtools.TestCase,
    )

classes = documentationtools.list_all_abjad_classes(
    ignored_classes=ignored_classes,
    )


@pytest.mark.parametrize('obj', classes)
def test_abjad___doc___01(obj):
    r'''All classes have a docstring. All class methods have a docstring.
    '''
    missing_doc_names = []
    if obj.__doc__ is None:
        missing_doc_names.append(obj.__name__)
    for attr in inspect.classify_class_attrs(obj):
        if attr.name in ignored_names:
            continue
        elif attr.defining_class is not obj:
            continue
        if attr.name[0].isalpha() or attr.name.startswith('__'):
            if getattr(obj, attr.name).__doc__ is None:
                missing_doc_names.append(attr.name)
    if missing_doc_names:
        message = '\n'.join('{}.{}'.format(obj.__name__, name)
            for name in missing_doc_names)
        message = 'Missing docstrings for:\n{}'.format(message)
        raise Exception(message)


functions = documentationtools.list_all_abjad_functions()


@pytest.mark.parametrize('obj', functions)
def test_abjad___doc___02(obj):
    r'''All functions have a docstring.
    '''
    assert obj.__doc__ is not None
