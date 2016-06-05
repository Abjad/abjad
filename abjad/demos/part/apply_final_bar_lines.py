# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def apply_final_bar_lines(score):
    r'''Applies final bar lines to score.
    '''

    for voice in iterate(score).by_class(scoretools.Voice):
        bar_line = indicatortools.BarLine('|.')
        attach(bar_line, voice[-1])