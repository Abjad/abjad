from abjad import *


def apply_page_breaks(score):

    bell_voice = score['Bell Voice']

    measure_indices = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 72,
        79, 86, 93, 100]

    for measure_index in measure_indices:
        marktools.LilyPondCommandMark(
            'break',
            'after'
            )(bell_voice[measure_index])
