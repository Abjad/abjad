# -*- encoding: utf-8 -*-
import pytest
from abjad import *


def test_labeltools_label_vertical_moments_in_expr_with_interval_class_vectors_01():

    score = Score(Staff([]) * 3)
    notes = [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]
    score[0].extend(notes)
    clef = Clef('alto')
    attach(clef, score[1])
    score[1].extend([Note(-5, (1, 4)), Note(-7, (1, 4))])
    clef = Clef('bass')
    attach(clef, score[2])
    score[2].append(Note(-24, (1, 2)))
    labeltools.label_vertical_moments_in_expr_with_interval_class_vectors(
        score)

    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                c'8
                d'8
                    _ \markup {
                        \tiny
                            0010020
                        }
                e'8
                f'8
                    _ \markup {
                        \tiny
                            1000020
                        }
            }
            \new Staff {
                \clef "alto"
                g4
                f4
                    _ \markup {
                        \tiny
                            0100110
                        }
            }
            \new Staff {
                \clef "bass"
                c,2
                    _ \markup {
                        \tiny
                            1000020
                        }
            }
        >>
        '''
        )

    assert inspect_(score).is_well_formed()


def test_labeltools_label_vertical_moments_in_expr_with_interval_class_vectors_02():
    r'''Vertical moments with quartertones format with a two-row
    interval-class vector. Top for 12-ET, bottom for 24-ET.
    '''
    pytest.skip('make work with quartertones again.')

    chord = Chord([-2, -1.5, 9], (1, 4))
    labeltools.label_vertical_moments_in_expr_with_interval_class_vectors(
        chord)

    assert systemtools.TestManager.compare(
        chord,
        r'''
        <bf bqf a'>4
            _ \markup {
                \tiny
                    \column
                        {
                            0100000
                            110000
                        }
                }
        '''
        )

    assert inspect_(chord).is_well_formed()