# -*- encoding: utf-8 -*-
from abjad import *
import pytest


def test_scoretools_FixedDurationContainer_format_01():

    container = scoretools.FixedDurationContainer((3, 8), "c'8 d'8 e'8")
    assert systemtools.TestManager.compare(
        container,
        r'''
        {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_scoretools_FixedDurationContainer_format_02():

    container = scoretools.FixedDurationContainer((3, 8), "c'8 d'8")
    assert pytest.raises(Exception, 'container.format')


def test_scoretools_FixedDurationContainer_format_03():

    container = scoretools.FixedDurationContainer((3, 8), "c'8 d'8 e'8 f'8")
    assert pytest.raises(Exception, 'container.format')
