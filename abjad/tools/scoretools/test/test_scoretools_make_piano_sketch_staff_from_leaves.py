# -*- coding: utf-8 -*-
from abjad import *


def test_scoretools_make_piano_sketch_staff_from_leaves_01():

    notes = scoretools.make_notes([-12, -10, -8, -7, -5, 0, 2, 4, 5, 7], [(1, 4)])
    score, treble_staff, bass_staff = scoretools.make_piano_sketch_score_from_leaves(notes)

    r'''
    \new Score \with {
        \override BarLine.stencil = ##f
        \override BarNumber.transparent = ##t
        \override SpanBar.stencil = ##f
        \override TimeSignature.stencil = ##f
    } <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                r4
                r4
                r4
                r4
                r4
                c'4
                d'4
                e'4
                f'4
                g'4
            }
            \context Staff = "bass" {
                \clef "bass"
                c4
                d4
                e4
                f4
                g4
                r4
                r4
                r4
                r4
                r4
            }
        >>
    >>
    '''

    assert format(score) == stringtools.normalize(
        r'''
        \new Score \with {
            \override BarLine.stencil = ##f
            \override BarNumber.transparent = ##t
            \override SpanBar.stencil = ##f
            \override TimeSignature.stencil = ##f
        } <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    r4
                    r4
                    r4
                    r4
                    r4
                    c'4
                    d'4
                    e'4
                    f'4
                    g'4
                }
                \context Staff = "bass" {
                    \clef "bass"
                    c4
                    d4
                    e4
                    f4
                    g4
                    r4
                    r4
                    r4
                    r4
                    r4
                }
            >>
        >>
        '''
        )
