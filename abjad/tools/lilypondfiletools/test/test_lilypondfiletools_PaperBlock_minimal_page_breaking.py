# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_PaperBlock_minimal_page_breaking_01():

    paper_block = lilypondfiletools.PaperBlock()
    paper_block.minimal_page_breaking = True

    assert systemtools.TestManager.compare(
        paper_block,
        r'''
        \paper {
            #(define page-breaking ly:minimal-breaking)
        }
        '''
        )
