# -*- encoding: utf-8 -*-
from abjad import *


def apply_final_bar_lines(score):

    for voice in iterationtools.iterate_voices_in_expr(score):
        bar_line = marktools.BarLine('|.')
        bar_line.attach(voice[-1])
