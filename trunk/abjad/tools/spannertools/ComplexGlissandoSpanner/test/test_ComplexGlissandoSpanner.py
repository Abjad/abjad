# -*- encoding: utf-8 -*-
from abjad import *


def test_ComplexGlissandoSpanner_01():
    t = Staff("c'8 d'8 r8 e'8")
    gliss = spannertools.ComplexGlissandoSpanner(t.select_leaves()[:])
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
        t.lilypond_format,
        "\\new Staff {\n\tc'8 \\glissando\n\td'8 \\glissando\n\t\\once \\override NoteColumn #'glissando-skip = ##t\n\t\\once \\override Rest #'transparent = ##t\n\tr8\n\te'8\n}"
        )
