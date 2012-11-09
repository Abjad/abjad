from abjad import *
import py


def test_TaleaFilledRhythmMaker_tie_split_notes_01():
    py.test.skip('working on this one now.')

    leaves = leaftools.make_leaves_from_talea([1, 1, 2, -2, 4, -4, 5, -5], 16)
    maker = rhythmmakertools.TaleaFilledRhythmMaker([5], 16, tie_split_notes=True)
    divisions = [(2, 8), (2, 8), (2, 8), (2, 8)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
    staff = Staff(measures)
    measures = measuretools.replace_contents_of_measures_in_expr(staff, music)

    #f(staff)
