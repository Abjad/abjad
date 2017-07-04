# -*- coding: utf-8 -*-
import pytest
from abjad import *
from abjad.tools.lilypondparsertools import LilyPondParser


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_01():

    target = Score([Staff([Note(0, 1)])])
    mark = MetronomeMark(textual_indication="As fast as possible")
    attach(mark, target[0], scope=Staff)

    assert format(target) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo "As fast as possible"
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = select(result).by_leaf()
    leaf = leaves[0]
    marks = inspect_(leaf).get_indicators(MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_02():

    target = Score([Staff([Note(0, 1)])])
    leaves = select(target).by_leaf()
    mark = MetronomeMark((1, 4), 60)
    attach(mark, leaves[0], scope=Staff)

    assert format(target) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=60
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = select(result).by_leaf()
    leaf = leaves[0]
    marks = inspect_(leaf).get_indicators(MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_03():

    target = Score([Staff([Note(0, 1)])])
    leaves = select(target).by_leaf()
    mark = MetronomeMark((1, 4), (59, 63))
    attach(mark, leaves[0], scope=Staff)

    assert format(target) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=59-63
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = select(result).by_leaf()
    leaf = leaves[0]
    marks = inspect_(leaf).get_indicators(MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_04():

    target = Score([Staff([Note(0, 1)])])
    mark = MetronomeMark(
        reference_duration=(1, 4),
        units_per_minute=60,
        textual_indication="Like a majestic swan, alive with youth and vigour!",
        )
    leaves = select(target).by_leaf()
    attach(mark, leaves[0], scope=Staff)

    assert format(target) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo "Like a majestic swan, alive with youth and vigour!" 4=60
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = select(result).by_leaf()
    leaf = leaves[0]
    marks = inspect_(leaf).get_indicators(MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_05():

    target = Score([Staff([Note(0, 1)])])
    mark = MetronomeMark(
        reference_duration=(1, 16), 
        units_per_minute=(34, 55),
        textual_indication="Faster than a thousand suns",
        )
    leaves = select(target).by_leaf()
    attach(mark, leaves[0], scope=Staff)

    assert format(target) == stringtools.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo "Faster than a thousand suns" 16=34-55
                c'1
            }
        >>
        '''
        )

    parser = LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = select(result).by_leaf()
    leaf = leaves[0]
    marksn = inspect_(leaf).get_indicators(MetronomeMark)
    assert len(marksn) == 1
