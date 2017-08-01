# -*- coding: utf-8 -*-
import abjad
import pytest


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_01():

    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    mark = abjad.MetronomeMark(textual_indication="As fast as possible")
    abjad.attach(mark, target[0][0], scope=abjad.Staff)

    assert format(target) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo "As fast as possible"
                c'1
            }
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = abjad.select(result).by_leaf()
    leaf = leaves[0]
    marks = abjad.inspect(leaf).get_indicators(abjad.MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_02():

    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    leaves = abjad.select(target).by_leaf()
    mark = abjad.MetronomeMark((1, 4), 60)
    abjad.attach(mark, leaves[0], scope=abjad.Staff)

    assert format(target) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=60
                c'1
            }
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = abjad.select(result).by_leaf()
    leaf = leaves[0]
    marks = abjad.inspect(leaf).get_indicators(abjad.MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_03():

    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    leaves = abjad.select(target).by_leaf()
    mark = abjad.MetronomeMark((1, 4), (59, 63))
    abjad.attach(mark, leaves[0], scope=abjad.Staff)

    assert format(target) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo 4=59-63
                c'1
            }
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = abjad.select(result).by_leaf()
    leaf = leaves[0]
    marks = abjad.inspect(leaf).get_indicators(abjad.MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_04():

    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    mark = abjad.MetronomeMark(
        reference_duration=(1, 4),
        units_per_minute=60,
        textual_indication="Like a majestic swan, alive with youth and vigour!",
        )
    leaves = abjad.select(target).by_leaf()
    abjad.attach(mark, leaves[0], scope=abjad.Staff)

    assert format(target) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo "Like a majestic swan, alive with youth and vigour!" 4=60
                c'1
            }
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = abjad.select(result).by_leaf()
    leaf = leaves[0]
    marks = abjad.inspect(leaf).get_indicators(abjad.MetronomeMark)
    assert len(marks) == 1


def test_lilypondparsertools_LilyPondParser__indicators__MetronomeMark_05():

    target = abjad.Score([abjad.Staff([abjad.Note(0, 1)])])
    mark = abjad.MetronomeMark(
        reference_duration=(1, 16), 
        units_per_minute=(34, 55),
        textual_indication="Faster than a thousand suns",
        )
    leaves = abjad.select(target).by_leaf()
    abjad.attach(mark, leaves[0], scope=abjad.Staff)

    assert format(target) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \tempo "Faster than a thousand suns" 16=34-55
                c'1
            }
        >>
        '''
        )

    parser = abjad.lilypondparsertools.LilyPondParser()
    result = parser(format(target))
    assert format(target) == format(result) and target is not result
    leaves = abjad.select(result).by_leaf()
    leaf = leaves[0]
    marksn = abjad.inspect(leaf).get_indicators(abjad.MetronomeMark)
    assert len(marksn) == 1
