from scf import specifiers
import scf


def test_ClefSpecifierEditor_run_01():

    editor = scf.editors.ClefSpecifierEditor()
    editor.run(user_input='clef tre done') == 'treble'
