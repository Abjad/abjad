from abjad import *


def apply_expressive_marks(score):

    bell_voice = score['Bell Voice']
    marktools.BarLine('|.')(bell_voice[-1])
