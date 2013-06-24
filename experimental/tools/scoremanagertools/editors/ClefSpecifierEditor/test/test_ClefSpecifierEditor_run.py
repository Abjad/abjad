from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_ClefSpecifierEditor_run_01():

    editor = scoremanagertools.editors.ClefSpecifierEditor()
    editor._run(pending_user_input='clef tre done') == 'treble'
