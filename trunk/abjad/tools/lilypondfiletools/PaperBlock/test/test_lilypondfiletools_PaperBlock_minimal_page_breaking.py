# -*- encoding: utf-8 -*-
from abjad import *


def test_lilypondfiletools_PaperBlock_minimal_page_breaking_01():

    pb = lilypondfiletools.PaperBlock()
    pb.minimal_page_breaking = True

    r'''
    \paper {
        #(define page-breaking ly:minimal-breaking)
    }
    '''

    assert testtools.compare(
        pb,
        r'''
        \paper {
            #(define page-breaking ly:minimal-breaking)
        }
        '''
        )
