# -*- encoding: utf-8 -*-
import os
from abjad import *
from output_material import example_numbers


def __illustrate__(example_numbers):
    notes = scoretools.make_notes(example_numbers, [Duration(1, 8)])
    result = scoretools.make_piano_score_from_leaves(notes)
    score, treble_staff, bass_staff = result
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    return lilypond_file


if __name__ == '__main__':
    lilypond_file = __illustrate__(example_numbers)
    file_path = os.path.abspath(__file__)
    directory_path = os.path.dirname(file_path)
    file_path = os.path.join(directory_path, 'illustration.pdf')
    persist(lilypond_file).as_pdf(file_path) 
