# -*- encoding: utf-8 -*-
from abjad import *


def test_BracketSpanner___init___01():
    r'''Init empty bracket spanner.
    '''

    bracket = spannertools.BracketSpanner()
    assert isinstance(bracket, spannertools.BracketSpanner)


def test_BracketSpanner___init___02():
    r'''Bracket defaults to solid red line with left and right nibs
    and with no nibs at left and right broken edges.
    '''

    staff = Staff(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(staff)
    spannertools.BracketSpanner(staff[1])
    measuretools.set_always_format_time_signature_of_measures_in_expr(staff)

    assert testtools.compare(
        staff,
        r'''
        \new Staff {
            {
                \time 2/8
                c'8
                d'8
            }
            {
                \time 2/8
                \override TextSpanner #'bound-details #'left #'text = \markup { \draw-line #'(0 . -1) }
                \override TextSpanner #'bound-details #'left-broken #'text = ##f
                \override TextSpanner #'bound-details #'right #'text = \markup { \draw-line #'(0 . -1) }
                \override TextSpanner #'bound-details #'right-broken #'text = ##f
                \override TextSpanner #'color = #red
                \override TextSpanner #'dash-fraction = #1
                \override TextSpanner #'staff-padding = #2
                \override TextSpanner #'thickness = #1.5
                e'8 \startTextSpan
                f'8 \stopTextSpan
                \revert TextSpanner #'bound-details
                \revert TextSpanner #'color
                \revert TextSpanner #'dash-fraction
                \revert TextSpanner #'staff-padding
                \revert TextSpanner #'thickness
            }
            {
                \time 2/8
                g'8
                a'8
            }
        }
        '''
        )
