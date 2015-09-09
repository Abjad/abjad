# -*- coding: utf-8 -*-
import pytest
from abjad import *


# NOTE: all tests operate on the following expression
staff = Staff(
    r'''
    c'8
    cs'8
    <<
        \new Voice {
            d'8
            ef'8
        }
        \new Voice {
            e'8
            f'8
        }
    >>
    fs'8
    g'8
    '''
    )


def test_agenttools_IterationAgent_depth_first_01():
    '''
    Default depth-first search:
        * capped iteration returns no elements above self._client
        * unique returns each node at most once
        * no classes forbidden means all containers entered
    '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff[2]).depth_first()

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][1][1]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    ef'8
    Voice(e'8, f'8)
    e'8
    f'8
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff[2]).depth_first(
        direction=Right,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][0][0]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    e'8
    Voice(d'8, ef'8)
    ef'8
    d'8
    '''


def test_agenttools_IterationAgent_depth_first_02():
    r'''Uncapped depth-first search: uncapped iteration returns
    all elements above self._client
    '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff
    assert next(iterator) is staff[3]
    assert next(iterator) is staff[4]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    ef'8
    Voice(e'8, f'8)
    e'8
    f'8
    Staff{5}
    fs'8
    iterator'8
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        direction=Right,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff
    assert next(iterator) is staff[1]
    assert next(iterator) is staff[0]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    e'8
    Voice(d'8, ef'8)
    ef'8
    d'8
    Staff{5}
    cs'8
    c'8
    '''


def test_agenttools_IterationAgent_depth_first_03():
    r'''Duplicates-allowed depth-first search: nodes yield every time they are
    traversed.  '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff[2]).depth_first(
        unique=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff[2]).depth_first(
        direction=Right,
        unique=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    '''


def test_agenttools_IterationAgent_depth_first_04():
    r'''Restricted depth-first search: iteration will yield -- but will not
    enter -- forbidden classes.
    '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff).depth_first(
        forbid='simultaneous',
        )

    assert next(iterator) is staff
    assert next(iterator) is staff[0]
    assert next(iterator) is staff[1]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff[3]
    assert next(iterator) is staff[4]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Staff{5}
    c'8
    cs'8
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    fs'8
    iterator'8
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff).depth_first(
        direction=Right,
        forbid='simultaneous',
        )

    assert next(iterator) is staff
    assert next(iterator) is staff[4]
    assert next(iterator) is staff[3]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff[1]
    assert next(iterator) is staff[0]
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Staff{5}
    iterator'8
    fs'8
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    cs'8
    c'8
    '''


def test_agenttools_IterationAgent_depth_first_05():
    r'''Uncapped depth-first search with duplicates allowed.
    '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        unique=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[3]
    assert next(iterator) is staff
    assert next(iterator) is staff[4]
    assert next(iterator) is staff
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    Staff{5}
    iterator'8
    Staff{5}
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        direction=Right,
        unique=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][1]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2][1][0]
    assert next(iterator) is staff[2][1]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][1]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2][0][0]
    assert next(iterator) is staff[2][0]
    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[1]
    assert next(iterator) is staff
    assert next(iterator) is staff[0]
    assert next(iterator) is staff
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(e'8, f'8)
    f'8
    Voice(e'8, f'8)
    e'8
    Voice(e'8, f'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Voice(d'8, ef'8)
    ef'8
    Voice(d'8, ef'8)
    d'8
    Voice(d'8, ef'8)
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    Staff{5}
    c'8
    Staff{5}
    '''


def test_agenttools_IterationAgent_depth_first_06():
    r'''Uncapped and restricted depth-first search.
    '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        forbid='simultaneous',
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[3]
    assert next(iterator) is staff[4]

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    iterator'8
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        direction=Right,
        forbid='simultaneous',
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[1]
    assert next(iterator) is staff[0]

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    c'8
    '''


def test_agenttools_IterationAgent_depth_first_07():
    r'''Restricted depth-first search with duplicates allowed.
    '''

    # LEFT-TO-RIGHT

    iterator = iterate(staff).depth_first(
        forbid='simultaneous',
        unique=False,
        )

    assert next(iterator) is staff
    assert next(iterator) is staff[0]
    assert next(iterator) is staff
    assert next(iterator) is staff[1]
    assert next(iterator) is staff
    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[3]
    assert next(iterator) is staff
    assert next(iterator) is staff[4]
    assert next(iterator) is staff
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Staff{5}
    c'8
    Staff{5}
    cs'8
    Staff{5}
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    Staff{5}
    iterator'8
    Staff{5}
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff).depth_first(
        direction=Right,
        forbid='simultaneous',
        unique=False,
        )

    assert next(iterator) is staff
    assert next(iterator) is staff[4]
    assert next(iterator) is staff
    assert next(iterator) is staff[3]
    assert next(iterator) is staff
    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[1]
    assert next(iterator) is staff
    assert next(iterator) is staff[0]
    assert next(iterator) is staff
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Staff{5}
    iterator'8
    Staff{5}
    fs'8
    Staff{5}
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    Staff{5}
    c'8
    Staff{5}
    '''


def test_agenttools_IterationAgent_depth_first_08():
    r'''Uncapped but restricted depth-first serach with duplicates allowed.
    '''

    # LEFT-TO-RIGHT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        forbid='simultaneous',
        unique=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[3]
    assert next(iterator) is staff
    assert next(iterator) is staff[4]
    assert next(iterator) is staff
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    fs'8
    Staff{5}
    iterator'8
    Staff{5}
    '''

    # RIGHT-TO-LEFT #

    iterator = iterate(staff[2]).depth_first(
        capped=False,
        direction=Right,
        forbid='simultaneous',
        unique=False,
        )

    assert next(iterator) is staff[2]
    assert next(iterator) is staff
    assert next(iterator) is staff[1]
    assert next(iterator) is staff
    assert next(iterator) is staff[0]
    assert next(iterator) is staff
    assert pytest.raises(StopIteration, 'next(iterator)')

    r'''
    Container(Voice(d'8, ef'8), Voice(e'8, f'8))
    Staff{5}
    cs'8
    Staff{5}
    c'8
    Staff{5}
    '''
