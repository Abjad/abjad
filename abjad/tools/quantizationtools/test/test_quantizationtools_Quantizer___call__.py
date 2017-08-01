# -*- coding: utf-8 -*-
import abjad
from abjad.tools import quantizationtools


def test_quantizationtools_Quantizer___call___01():
    milliseconds = [1500, 1500]
    q_events = quantizationtools.QEventSequence.from_millisecond_durations(
        milliseconds)
    quantizer = quantizationtools.Quantizer()
    result = quantizer(q_events)
    staff = abjad.Staff([result], context_name='RhythmicStaff')
    score = abjad.Score([staff])
    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new RhythmicStaff {
                \new Voice {
                    {
                        \time 4/4
                        \tempo 4=60
                        c'4.
                        c'4.
                        r4
                    }
                }
            }
        >>
        '''
        ), format(score)


def test_quantizationtools_Quantizer___call___02():
    milliseconds = [750, 750]
    q_events = quantizationtools.QEventSequence.from_millisecond_durations(
        milliseconds)
    quantizer = quantizationtools.Quantizer()
    optimizer = quantizationtools.MeasurewiseAttackPointOptimizer()
    result = quantizer(
        q_events,
        attack_point_optimizer=optimizer,
        )
    staff = abjad.Staff([result], context_name='RhythmicStaff')
    score = abjad.Score([staff])
    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new RhythmicStaff {
                \new Voice {
                    {
                        \time 4/4
                        \tempo 4=60
                        c'8.
                        c'16 ~
                        c'8
                        r8
                        r2
                    }
                }
            }
        >>
        '''
        ), format(score)


def test_quantizationtools_Quantizer___call___03():

    milliseconds = [1500, -1000, 1000, 1000, -1000, 1000, -1000, 500]
    sequence = quantizationtools.QEventSequence.from_millisecond_durations(milliseconds)
    attack_point_optimizer = quantizationtools.NullAttackPointOptimizer()
    quantizer = quantizationtools.Quantizer()

    result = quantizer(sequence, attack_point_optimizer=attack_point_optimizer)

    assert isinstance(result, abjad.Voice)
    assert abjad.inspect(result).get_duration() == 2

    score = abjad.Score([abjad.Staff([result])])

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new Staff {
                \new Voice {
                    {
                        \time 4/4
                        \tempo 4=60
                        c'4 ~
                        c'8
                        r8
                        r8
                        c'8 ~
                        c'8
                        c'8 ~
                    }
                    {
                        c'8
                        r8
                        r8
                        c'8 ~
                        c'8
                        r8
                        r8
                        c'8
                    }
                }
            }
        >>
        '''
        ), format(score)


def test_quantizationtools_Quantizer___call___04():

    milliseconds = [250, 1000, 1000, 1000, 750]
    sequence = quantizationtools.QEventSequence.from_millisecond_durations(
        milliseconds)
    attack_point_optimizer = quantizationtools.NullAttackPointOptimizer()
    quantizer = quantizationtools.Quantizer()
    result = quantizer(sequence, attack_point_optimizer=attack_point_optimizer)
    staff = abjad.Staff([result], context_name='RhythmicStaff')
    score = abjad.Score([staff])

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new RhythmicStaff {
                \new Voice {
                    {
                        \time 4/4
                        \tempo 4=60
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
            }
        >>
        '''
        ), format(score)


def test_quantizationtools_Quantizer___call___05():

    q_schema = quantizationtools.BeatwiseQSchema(
        {'search_tree': quantizationtools.UnweightedSearchTree({2: None})},
        {'search_tree': quantizationtools.UnweightedSearchTree({3: None})},
        {'search_tree': quantizationtools.UnweightedSearchTree({5: None})},
        {'search_tree': quantizationtools.UnweightedSearchTree({7: None})},
        )
    milliseconds = [250, 250, 250, 250] * 4
    q_events = quantizationtools.QEventSequence.from_millisecond_durations(
        milliseconds)
    attack_point_optimizer = quantizationtools.NullAttackPointOptimizer()
    quantizer = quantizationtools.Quantizer()

    result = quantizer(
        q_events,
        q_schema=q_schema,
        attack_point_optimizer=attack_point_optimizer,
        )
    staff = abjad.Staff([result], context_name='RhythmicStaff')
    score = abjad.Score([staff])

    assert format(score) == abjad.String.normalize(
        r'''
        \new Score <<
            \new RhythmicStaff {
                \new Voice {
                    \grace {
                        c'16
                    }
                    \tempo 4=60
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
            }
        >>
        '''
        ), format(score)
