# -*- encoding: utf-8 -*-
from abjad import *


def test_pitchtools_insert_and_transpose_nested_subruns_in_pitch_class_number_list_01():

    notes = [Note(p, (1, 4)) for p in [0, 2, 7, 9, 5, 11, 4]]
    subrun_tokens = [(0, [2, 4]), (4, [3, 1])]
    pitchtools.insert_and_transpose_nested_subruns_in_pitch_class_number_list(
        notes, subrun_tokens)

    "Inserts are shown in the innermost pairs of brackets below."

    t = []
    for x in notes:
        try:
            t.append(x.written_pitch.pitch_class_number)
        except AttributeError:
            t.append([y.written_pitch.pitch_class_number for y in x])

    print t

    assert t == [0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]

    t = sequencetools.flatten_sequence(t)

    assert t == [0, 5, 7, 2, 4, 0, 6, 11, 7, 9, 5, 10, 6, 8, 11, 7, 4]
