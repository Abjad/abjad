from experimental.tools.scftools import specifiers
from experimental import *


def test_ClefSpecifierEditor_run_01():

    editor = scftools.editors.ClefSpecifierEditor()
    editor.run(user_input='clef tre done') == 'treble'
