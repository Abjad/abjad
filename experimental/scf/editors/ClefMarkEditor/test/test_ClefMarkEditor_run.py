from abjad.tools import contexttools
import scf


def test_ClefMarkEditor_run_01():

    editor = scf.editors.ClefMarkEditor()
    editor.run(user_input='clef treble done')

    clef_mark = contexttools.ClefMark('treble')
    assert editor.target == clef_mark
