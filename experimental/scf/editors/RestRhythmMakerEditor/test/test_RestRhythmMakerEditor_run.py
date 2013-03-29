from abjad.tools import rhythmmakertools
import scf


def test_RestRhythmMakerEditor_run_01():

    editor = scf.editors.RestRhythmMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.RestRhythmMaker()

    assert editor.target == maker
