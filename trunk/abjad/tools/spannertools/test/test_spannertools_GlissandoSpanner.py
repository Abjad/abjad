# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_GlissandoSpanner_01():

    staff = Staff([Note(n, (1, 8)) for n in range(8)])
    glissando = spannertools.GlissandoSpanner()
    glissando.attach(staff.select_leaves()[:4])

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \glissando
            cs'8 \glissando
            d'8 \glissando
            ef'8
            e'8
            f'8
            fs'8
            g'8
        }
        '''
        )
