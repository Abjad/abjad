# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools import systemtools


def test_scoretools_make_piano_score_from_leaves_01():
    r'''Works with notes.
    '''

    pitches = [-12, 37, -10, 27, 4, 17]
    notes = [Note(x, (1, 4)) for x in pitches]
    score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(notes)

    r"""
    \new Score <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                r4
                cs''''4
                r4
                ef'''4
                e'4
                f''4
            }
            \context Staff = "bass" {
                \clef "bass"
                c4
                r4
                d4
                r4
                r4
                r4
            }
        >>
    >>
    """

    assert inspect_(score).is_well_formed()
    assert format(score) == stringtools.normalize(
        r"""
        \new Score <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    r4
                    cs''''4
                    r4
                    ef'''4
                    e'4
                    f''4
                }
                \context Staff = "bass" {
                    \clef "bass"
                    c4
                    r4
                    d4
                    r4
                    r4
                    r4
                }
            >>
        >>
        """
        )


def test_scoretools_make_piano_score_from_leaves_02():
    r'''Works with explicit lowest treble pitch.
    '''

    container = topleveltools.parse("{ g4 a4 b4 c'4 d'4 r4 a4 g4 }")
    container_contents = container[:]
    del(container[:])
    lowest_treble_pitch = NamedPitch('a')
    score, treble_staff, bass_staff = \
        scoretools.make_piano_score_from_leaves(
        container_contents,
        lowest_treble_pitch=lowest_treble_pitch,
        )

    r'''
    \new Score <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                r4
                a4
                b4
                c'4
                d'4
                r4
                a4
                r4
            }
            \context Staff = "bass" {
                \clef "bass"
                g4
                r4
                r4
                r4
                r4
                r4
                r4
                g4
            }
        >>
    >>
    '''

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                    r4
                    a4
                    b4
                    c'4
                    d'4
                    r4
                    a4
                    r4
                }
                \context Staff = "bass" {
                    \clef "bass"
                    g4
                    r4
                    r4
                    r4
                    r4
                    r4
                    r4
                    g4
                }
            >>
        >>
        '''
        )
