# -*- encoding: utf-8 -*-
from abjad import *


def apply_final_bar_lines(score):
    r'''Applies final bar lines to score.
    '''

    for voice in iterate(score).by_class(scoretools.Voice):
        bar_line = indicatortools.BarLine('|.')
        attach(bar_line, voice[-1])