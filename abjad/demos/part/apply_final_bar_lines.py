# -*- encoding: utf-8 -*-
from abjad import *


def apply_final_bar_lines(score):

    for voice in iterationtools.iterate_voices_in_expr(score):
        bar_line = marktools.BarLine('|.')
        attach(bar_line, voice[-1])
