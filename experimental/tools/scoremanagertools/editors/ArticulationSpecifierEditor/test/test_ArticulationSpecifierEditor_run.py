from experimental import *


def test_ArticulationSpecifierEditor_run_01():

    editor = scoremanagertools.editors.ArticulationSpecifierEditor()
    editor._run(user_input='artic experimental.tools.scoremanagertools.materialpackages.red_mar done')
    specifier = scoremanagertools.specifiers.ArticulationSpecifier(
        articulation_handler_name='experimental.tools.scoremanagertools.materialpackages.red_marcati')

    assert editor.target == specifier
