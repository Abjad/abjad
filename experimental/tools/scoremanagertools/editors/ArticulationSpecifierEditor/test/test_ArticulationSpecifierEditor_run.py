from experimental.tools.scoremanagertools import specifiers
from experimental import *


def test_ArticulationSpecifierEditor_run_01():

    editor = scoremanagertools.editors.ArticulationSpecifierEditor()
    editor._run(user_input='artic built_in_materials.red_mar done')
    specifier = specifiers.ArticulationSpecifier(articulation_handler_name='built_in_materials.red_marcati')

    assert editor.target == specifier
