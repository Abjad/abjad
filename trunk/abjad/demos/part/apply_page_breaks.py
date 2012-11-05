from abjad import *


def apply_page_breaks(score):

    bell_voice = score['Bell Voice']

    break_measures = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 72,
        79, 86, 93, 100]

    for break_measure in break_measures:
        marktools.LilyPondCommandMark('break', 'after')(bell_voice[break_measure])
