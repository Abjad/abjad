from scf import specifiers
import scf


def test_MusicSpecifierEditor_run_01():

    editor = scf.editors.MusicSpecifierEditor()
    editor.run(user_input='q')

    assert editor.target == specifiers.MusicSpecifier([])
    assert editor.target.format == 'specifiers.MusicSpecifier([])'
