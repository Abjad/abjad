# -*- encoding: utf-8 -*-
from abjad import *


def test_spannertools_ComplexGlissandoSpanner_01():

    staff = Staff("c'8 d'8 r8 e'8")
    glissando = spannertools.ComplexGlissandoSpanner()
    glissando.attach(staff.select_leaves())

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            c'8 \glissando
            d'8 \glissando
            \once \override NoteColumn #'glissando-skip = ##t
            \once \override Rest #'transparent = ##t
            r8
            e'8
        }
        '''
        )
