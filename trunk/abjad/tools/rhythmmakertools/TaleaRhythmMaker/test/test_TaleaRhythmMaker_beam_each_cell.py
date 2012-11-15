from abjad import *


def test_TaleaRhythmMaker_beam_each_cell_01():
    '''Beam each cell with a multipart beam spanner.
    '''

    talea, talea_denominator, prolation_addenda = [1, 1, 1, -1, 2, 2], 32, [3, 4]
    maker = rhythmmakertools.TaleaRhythmMaker(
        talea, talea_denominator, prolation_addenda, beam_each_cell=True)

    divisions = [(2, 16), (5, 16)]
    music = maker(divisions)

    music = sequencetools.flatten_sequence(music)
    measures = measuretools.make_measures_with_full_measure_spacer_skips(divisions)
    staff = Staff(measures)
    measuretools.replace_contents_of_measures_in_expr(staff, music)
    score = Score([staff])
    score.set.autoBeaming = False

    assert score.lilypond_format == "\\new Score \\with {\n\tautoBeaming = ##f\n} <<\n\t\\new Staff {\n\t\t{\n\t\t\t\\time 2/16\n\t\t\t\\times 4/7 {\n\t\t\t\tc'32 [\n\t\t\t\tc'32\n\t\t\t\tc'32 ]\n\t\t\t\tr32\n\t\t\t\tc'16 [\n\t\t\t\tc'32 ]\n\t\t\t}\n\t\t}\n\t\t{\n\t\t\t\\time 5/16\n\t\t\t\\fraction \\times 5/7 {\n\t\t\t\tc'32 [\n\t\t\t\tc'32\n\t\t\t\tc'32\n\t\t\t\tc'32 ]\n\t\t\t\tr32\n\t\t\t\tc'16 [\n\t\t\t\tc'16\n\t\t\t\tc'32\n\t\t\t\tc'32\n\t\t\t\tc'32 ]\n\t\t\t\tr32\n\t\t\t\tc'32\n\t\t\t}\n\t\t}\n\t}\n>>"
