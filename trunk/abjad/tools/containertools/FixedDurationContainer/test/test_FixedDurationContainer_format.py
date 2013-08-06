# -*- encoding: utf-8 -*-
from abjad import *
import py


def test_FixedDurationContainer_format_01():

    container = containertools.FixedDurationContainer((3, 8), "c'8 d'8 e'8")
    assert testtools.compare(
        container.lilypond_format,
        r'''
        {
            c'8
            d'8
            e'8
        }
        '''
        )


def test_FixedDurationContainer_format_02():

    container = containertools.FixedDurationContainer((3, 8), "c'8 d'8")
    assert py.test.raises(Exception, 'container.format')


def test_FixedDurationContainer_format_03():

    container = containertools.FixedDurationContainer((3, 8), "c'8 d'8 e'8 f'8")
    assert py.test.raises(Exception, 'container.format')
