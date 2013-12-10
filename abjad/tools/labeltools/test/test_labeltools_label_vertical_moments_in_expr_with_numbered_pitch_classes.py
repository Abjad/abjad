# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_vertical_moments_in_expr_with_numbered_pitch_classes_01():

    score = Score(Staff([]) * 3)
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    score[0].extend(notes)
    clef = Clef('alto')
    attach(clef, score[1])
    score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
    clef = Clef('bass')
    attach(clef, score[2])
    score[2].append(Note(-24, (1, 2)))
    labeltools.label_vertical_moments_in_expr_with_numbered_pitch_classes(
        score)

    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                c'8
                d'8
                    _ \markup {
                        \small
                            \column
                                {
                                    7
                                    2
                                    0
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    5
                                    0
                                }
                        }
            }
            \new Staff {
                \clef "alto"
                g4
                f4
                    _ \markup {
                        \small
                            \column
                                {
                                    5
                                    4
                                    0
                                }
                        }
            }
            \new Staff {
                \clef "bass"
                c,2
                    _ \markup {
                        \small
                            \column
                                {
                                    7
                                    0
                                }
                        }
            }
        >>
        '''
        )

    assert inspect(score).is_well_formed()
