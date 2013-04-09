from scftools import specifiers
import scftools


def test_MusicSpecifierEditor_run_01():

    editor = scftools.editors.MusicSpecifierEditor()
    editor.run(user_input='q')

    assert editor.target == specifiers.MusicSpecifier([])
    assert editor.target.format == 'specifiers.MusicSpecifier([])'
