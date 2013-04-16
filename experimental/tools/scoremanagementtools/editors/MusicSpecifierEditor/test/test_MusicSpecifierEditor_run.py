from experimental.tools.scoremanagementtools import specifiers
from experimental import *


def test_MusicSpecifierEditor_run_01():

    editor = scoremanagementtools.editors.MusicSpecifierEditor()
    editor.run(user_input='q')

    assert editor.target == specifiers.MusicSpecifier([])
    assert editor.target.format == 'specifiers.MusicSpecifier([])'
