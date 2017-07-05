# -*- coding: utf-8 -*-
import abjad


def apply_final_bar_lines(score):
    r'''Applies final bar lines to score.
    '''

    for voice in abjad.iterate(score).by_class(abjad.Voice):
        bar_line = abjad.BarLine('|.')
        abjad.attach(bar_line, voice[-1])
