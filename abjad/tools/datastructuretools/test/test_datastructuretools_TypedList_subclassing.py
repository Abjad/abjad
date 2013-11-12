# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.datastructuretools.TypedList import TypedList


class SpecialObjectInventory(TypedList):
    def __init__(self, *args, **kwargs):
        self.flavor = kwargs.get('flavor', None)
        self.color = kwargs.get('color', None)
        kwargs.pop('flavor', None)
        kwargs.pop('color', None)
        TypedList.__init__(self, *args, **kwargs)
    @property
    def _keyword_argument_names(self):
        result = []
        result.extend(TypedList._keyword_argument_names.fget(self))
        result.extend(['custom_identifier', 'flavor', 'color'])
        return tuple(sorted(result))
    @property
    def _tools_package_name(self):
        return 'specialtools'


def test_datastructuretools_TypedList_subclassing_01():
    r'''Inherited keyword argument names.
    '''

    foo = SpecialObjectInventory([])
    assert foo._keyword_argument_names == (
        'color', 
        'custom_identifier',
        'flavor',
        )


def test_datastructuretools_TypedList_subclassing_02():
    r'''Empty inventory. No keywords.
    '''

    foo = SpecialObjectInventory([])

    assert repr(foo) == 'SpecialObjectInventory([])'
    assert systemtools.TestManager.compare(
        foo._tools_package_qualified_indented_repr,
        'specialtools.SpecialObjectInventory([])',
        )


def test_datastructuretools_TypedList_subclassing_03():
    r'''Empty inventory. With keywords.
    '''

    foo = SpecialObjectInventory(custom_identifier='foo', color='red')

    assert repr(foo) == "SpecialObjectInventory([], color='red', custom_identifier='foo')"
    assert systemtools.TestManager.compare(
        foo._tools_package_qualified_indented_repr,
        r'''
        specialtools.SpecialObjectInventory([],
            color='red',
            custom_identifier='foo',
            )
        ''',
        )


def test_datastructuretools_TypedList_subclassing_04():
    r'''Populated inventory. No keywords.
    '''

    foo = SpecialObjectInventory(['foo', 99])

    assert systemtools.TestManager.compare(
        repr(foo),
        r'''
        SpecialObjectInventory(['foo', 99])
        ''',
        )
    assert systemtools.TestManager.compare(
        foo._tools_package_qualified_indented_repr,
        r'''
        specialtools.SpecialObjectInventory([
            'foo',
            99,
            ])
        ''',
        )


def test_datastructuretools_TypedList_subclassing_05():
    r'''Populated inventory. With keywords.
    '''

    foo = SpecialObjectInventory(['foo', 99], custom_identifier='foo', color='red')

    assert systemtools.TestManager.compare(
        repr(foo),
        r'''
        SpecialObjectInventory(['foo', 99], color='red', custom_identifier='foo')
        ''',
        )
    assert systemtools.TestManager.compare(
        foo._tools_package_qualified_indented_repr,
        r'''
        specialtools.SpecialObjectInventory([
            'foo',
            99,
            ],
            color='red',
            custom_identifier='foo',
            )
        ''',
        )
