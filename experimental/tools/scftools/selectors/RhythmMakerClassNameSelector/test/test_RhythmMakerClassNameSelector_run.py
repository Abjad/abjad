from experimental import *


def test_RhythmMakerClassNameSelector_run_01():

    selector = scftools.selectors.RhythmMakerClassNameSelector()

    assert selector.run(user_input='note') == 'NoteRhythmMaker'
