# -*- encoding: utf-8 -*-
from abjad import *


def test_leaftools_show_leaves_01():

    leaves = leaftools.make_leaves([None, 1, (-24, -22, 7, 21), None], (1, 4))
    score = leaftools.show_leaves(leaves, suppress_pdf=True)

    r'''
    \new Score \with {
        \override BarLine #'stencil = ##f
        \override BarNumber #'transparent = ##t
        \override SpanBar #'stencil = ##f
        \override TimeSignature #'stencil = ##f
    } <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                #(set-accidental-style 'forget)
                r4
                cs'4
                <g' a''>4
                r4
            }
            \context Staff = "bass" {
                \clef "bass"
                #(set-accidental-style 'forget)
                r4
                r4
                <c, d,>4
                r4
            }
        >>
    >>
    '''

    assert select(score).is_well_formed()
    assert testtools.compare(
        score,
        r'''
        \new Score \with {
            \override BarLine #'stencil = ##f
            \override BarNumber #'transparent = ##t
            \override SpanBar #'stencil = ##f
            \override TimeSignature #'stencil = ##f
        } <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    #(set-accidental-style 'forget)
                    r4
                    cs'4
                    <g' a''>4
                    r4
                }
                \context Staff = "bass" {
                    \clef "bass"
                    #(set-accidental-style 'forget)
                    r4
                    r4
                    <c, d,>4
                    r4
                }
            >>
        >>
        '''
        )
