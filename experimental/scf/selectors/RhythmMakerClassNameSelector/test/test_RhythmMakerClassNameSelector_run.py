import scf


def test_RhythmMakerClassNameSelector_run_01():

    selector = scf.selectors.RhythmMakerClassNameSelector()

    assert selector.run(user_input='note') == 'NoteRhythmMaker'
