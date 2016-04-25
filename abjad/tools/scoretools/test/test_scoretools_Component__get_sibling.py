# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_Component__get_sibling_01():
    '''Returns component when index is in range.
    '''

    staff = Staff("c' d' e' f'")
    assert staff[1]._get_sibling(2) is staff[3]
    assert staff[1]._get_sibling(1) is staff[2]
    assert staff[1]._get_sibling(0) is staff[1]
    assert staff[1]._get_sibling(-1) is staff[0]


def test_scoretools_Component__get_sibling_02():
    r'''Returns none when index is out of range.
    '''

    staff = Staff("c' d' e' f'")
    assert staff[1]._get_sibling(99) is None


def test_scoretools_Component__get_sibling_03():
    r'''Returns none when component has no parent.
    '''

    staff = Staff("c' d' e' f'")
    assert staff._get_sibling(1) is None
