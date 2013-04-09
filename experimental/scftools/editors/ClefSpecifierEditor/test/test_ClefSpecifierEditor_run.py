from scftools import specifiers
import scftools


def test_ClefSpecifierEditor_run_01():

    editor = scftools.editors.ClefSpecifierEditor()
    editor.run(user_input='clef tre done') == 'treble'
