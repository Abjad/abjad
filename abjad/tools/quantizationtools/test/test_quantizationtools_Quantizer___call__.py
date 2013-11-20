# -*- encoding: utf-8 -*-
from abjad import *


def test_quantizationtools_Quantizer___call___01():

    milliseconds = [1500, -1000, 1000, 1000, -1000, 1000, -1000, 500]
    sequence = quantizationtools.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = quantizationtools.NullAttackPointOptimizer()
    quantizer = quantizationtools.Quantizer()

    result = quantizer(sequence, attack_point_optimizer=attack_point_optimizer)

    assert isinstance(result, Voice)
    assert inspect(result).get_duration() == 2

    score = Score([Staff([result])])

    assert systemtools.TestManager.compare(
        score,
        r'''
        \new Score <<
            \new Staff {
                \new Voice {
                    {
                        \tempo 4=60
                        \time 4/4
                        c'4 ~
                        c'8
                        r8 ~
                        r8
                        c'8 ~
                        c'8
                        c'8 ~
                    }
                    {
                        c'8
                        r8 ~
                        r8
                        c'8 ~
                        c'8
                        r8 ~
                        r8
                        c'8
                    }
                }
            }
        >>
        '''
        )


def test_quantizationtools_Quantizer___call___02():

    milliseconds = [250, 1000, 1000, 1000, 750]
    sequence = quantizationtools.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = quantizationtools.NullAttackPointOptimizer()
    quantizer = quantizationtools.Quantizer()

    result = quantizer(sequence, attack_point_optimizer=attack_point_optimizer)

    assert systemtools.TestManager.compare(
        result,
        r'''
        \new Voice {
            {
                %%% \tempo 4=60 %%%
                \time 4/4
                c'16
                c'16 ~
                c'8 ~
                c'16
                c'16 ~
                c'8 ~
                c'16
                c'16 ~
                c'8 ~
                c'16
                c'16 ~
                c'8
            }
        }
        '''
        )


def test_quantizationtools_Quantizer___call___03():

    q_schema = quantizationtools.BeatwiseQSchema(
        {'search_tree': quantizationtools.UnweightedSearchTree({2: None})},
        {'search_tree': quantizationtools.UnweightedSearchTree({3: None})},
        {'search_tree': quantizationtools.UnweightedSearchTree({5: None})},
        {'search_tree': quantizationtools.UnweightedSearchTree({7: None})},
        )
    milliseconds = [250, 250, 250, 250] * 4
    sequence = quantizationtools.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = quantizationtools.NullAttackPointOptimizer()
    quantizer = quantizationtools.Quantizer()

    result = quantizer(sequence, q_schema=q_schema, attack_point_optimizer=attack_point_optimizer)

    assert systemtools.TestManager.compare(
        result,
        r'''
        \new Voice {
            \grace {
                c'16
            }
            %%% \tempo 4=60 %%%
            c'8
            \grace {
                c'16
            }
            c'8
            \times 2/3 {
                c'8
                \grace {
                    c'16
                }
                c'8
                c'8
            }
            \times 4/5 {
                c'16
                c'16
                c'16 ~
                c'16
                c'16
            }
            \times 4/7 {
                c'16 ~
                c'16
                c'16
                c'16 ~
                c'16
                c'16 ~
                c'16
            }
        }
        '''
        )
