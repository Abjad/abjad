# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_FixedDurationTuplet_trim_01():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    tuplet.trim(0)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            d'8
            e'8
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_scoretools_FixedDurationTuplet_trim_02():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    tuplet.trim(1)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'8
            e'8
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_scoretools_FixedDurationTuplet_trim_03():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    assert pytest.raises(Exception, 'tuplet.trim(99)')


def test_scoretools_FixedDurationTuplet_trim_04():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    tuplet.trim(0, 0)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'8
            d'8
            e'8
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_scoretools_FixedDurationTuplet_trim_05():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    tuplet.trim(0, 1)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            d'8
            e'8
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_scoretools_FixedDurationTuplet_trim_06():

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    tuplet.trim(1, 2)

    assert systemtools.TestManager.compare(
        tuplet,
        r'''
        \tweak #'text #tuplet-number::calc-fraction-text
        \times 4/3 {
            c'8
            e'8
        }
        '''
        )

    assert inspect(tuplet).is_well_formed()


def test_scoretools_FixedDurationTuplet_trim_07():
    r'''Trimming all leaves raises an exception.
    '''

    tuplet = scoretools.FixedDurationTuplet(Duration(2, 4), "c'8 d'8 e'8")
    tuplet.trim(1, 2)

    pytest.raises(Exception, 'tuplet.trim(0, 99)')
