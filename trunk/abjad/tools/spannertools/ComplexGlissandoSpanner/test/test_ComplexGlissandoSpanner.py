# -*- encoding: utf-8 -*-
from abjad import *


def test_ComplexGlissandoSpanner_01():
    staff = Staff("c'8 d'8 r8 e'8")
    gliss = spannertools.ComplexGlissandoSpanner(staff.select_leaves()[:])
    assert isinstance(gliss, spannertools.ComplexGlissandoSpanner)

    '''
    \new Staff {
        c'8 \glissando
        d'8 \glissando
        \once \override NoteColumn #'glissando-skip = ##t
        \once \override Rest #'transparent = ##t
        r8
        e'8
    }
    '''

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
