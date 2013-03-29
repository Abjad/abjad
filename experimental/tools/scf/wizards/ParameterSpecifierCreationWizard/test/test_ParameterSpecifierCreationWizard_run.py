from abjad import *
import scf


def test_ParameterSpecifierCreationWizard_run_01():

    wizard = scf.wizards.ParameterSpecifierCreationWizard()
    wizard.run(user_input='instrument instrument violin done')

    assert wizard.target == scf.specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())
