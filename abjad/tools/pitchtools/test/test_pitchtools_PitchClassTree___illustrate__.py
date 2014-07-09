# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassTree___illustrate___01():


    tree = pitchtools.PitchClassTree(
        items=[['c', 'e', 'g', 'af'], ['a', ['d', 'ef'], 'b']],
        item_class=pitchtools.NamedPitchClass,
        )
    lilypond_file = tree.__illustrate__()
    score = lilypond_file.score_block.items[0]

    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score \with {
            \override BarLine #'stencil = ##f
            \override Flag #'stencil = ##f
            \override Stem #'stencil = ##f
            \override TextScript #'staff-padding = #3
            \override TimeSignature #'stencil = ##f
        } <<
            \new Staff {
                \new Voice \with {
                    \consists Horizontal_bracket_engraver
                } {
                    c'8 \startGroup
                        ^ \markup {
                            \bold
                                {
                                    0
                                }
                            }
                    e'8
                    g'8
                    af'8 \stopGroup
                    a'8 \startGroup
                        ^ \markup {
                            \bold
                                {
                                    1
                                }
                            }
                    d'8 \startGroup
                    ef'8 \stopGroup
                    b'8 \stopGroup
                    \bar "|."
                }
            }
        >>
        '''
        ), format(score)