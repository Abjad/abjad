from scf import specifiers
import scf


def test_ArticulationSpecifierEditor_run_01():

    editor = scf.editors.ArticulationSpecifierEditor()
    editor.run(user_input='artic materials.red_mar done')
    specifier = specifiers.ArticulationSpecifier(articulation_handler_name='materials.red_marcati')

    assert editor.target == specifier
