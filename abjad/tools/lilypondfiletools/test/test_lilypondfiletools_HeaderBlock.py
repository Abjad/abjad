# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_HeaderBlock_01():

    header_block = lilypondfiletools.HeaderBlock()
    header_block.composer = markuptools.Markup('Josquin')
    header_block.title = markuptools.Markup('Missa sexti tonus')

    r'''
    \header {
        composer = \markup { Josquin }
        title = \markup { Missa sexti tonus }
    }
    '''

    assert systemtools.TestManager.compare(
        header_block,
        r'''
        \header {
            composer = \markup { Josquin }
            title = \markup { Missa sexti tonus }
        }
        '''
        )
