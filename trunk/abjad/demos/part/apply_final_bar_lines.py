from abjad.tools import iterationtools
from abjad.tools import marktools


def apply_final_bar_lines(score):

    for voice in iterationtools.iterate_voices_in_expr(score):
        marktools.BarLine('|.')(voice[-1])
