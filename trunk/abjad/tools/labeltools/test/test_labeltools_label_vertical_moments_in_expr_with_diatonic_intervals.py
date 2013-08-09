# -*- encoding: utf-8 -*-
from abjad import *


def test_labeltools_label_vertical_moments_in_expr_with_diatonic_intervals_01():

    score = Score(Staff([]) * 3)
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    score[0].extend(notes)
    contexttools.ClefMark('alto')(score[1])
    score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
    contexttools.ClefMark('bass')(score[2])
    score[2].append(Note(-24, (1, 2)))
    labeltools.label_vertical_moments_in_expr_with_diatonic_intervals(score)

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
                _ \markup {
                    \small
                        \column
                            {
                                16
                                12
                            }
                    }
            e'8
            f'8
                _ \markup {
                    \small
                        \column
                            {
                                18
                                11
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
                                17
                                11
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
                                15
                                12
                            }
                    }
        }
    >>
    '''

    assert select(score).is_well_formed()
    assert testtools.compare(
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
                                    16
                                    12
                                }
                        }
                e'8
                f'8
                    _ \markup {
                        \small
                            \column
                                {
                                    18
                                    11
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
                                    17
                                    11
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
                                    15
                                    12
                                }
                        }
            }
        >>
        '''
        )
