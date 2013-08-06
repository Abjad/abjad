# -*- encoding: utf-8 -*-
from abjad import *


def test_Staff_engraver_removals_01():

    t = Staff("c'8 d'8 e'8 f'8")
    t.engraver_removals.append('Time_signature_engraver')
    t.engraver_removals.append('Bar_number_engraver')

    r'''
    \new Staff \with {
        \remove Time_signature_engraver
        \remove Bar_number_engraver
    } {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    assert select(t).is_well_formed()
    assert testtools.compare(
        t.lilypond_format,
        r'''
        \new Staff \with {
            \remove Time_signature_engraver
            \remove Bar_number_engraver
        } {
            c'8
            d'8
            e'8
            f'8
        }
        '''
        )
