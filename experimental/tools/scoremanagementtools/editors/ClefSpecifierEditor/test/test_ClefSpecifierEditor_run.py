from experimental.tools.scoremanagementtools import specifiers
from experimental import *


def test_ClefSpecifierEditor_run_01():

    editor = scoremanagementtools.editors.ClefSpecifierEditor()
    editor.run(user_input='clef tre done') == 'treble'
