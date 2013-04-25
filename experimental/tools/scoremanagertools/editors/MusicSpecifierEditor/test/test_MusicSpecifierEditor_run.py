from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_MusicSpecifierEditor_run_01():

    editor = scoremanagertools.editors.MusicSpecifierEditor()
    editor.run(user_input='q')

    assert editor.target == specifiers.MusicSpecifier([])
    assert editor.target.format == 'specifiers.MusicSpecifier([])'
