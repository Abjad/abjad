from abjad import *
from experimental import *


def test_ParameterSpecifierCreationWizard_run_01():

    wizard = scftools.wizards.ParameterSpecifierCreationWizard()
    wizard.run(user_input='instrument instrument violin done')

    assert wizard.target == scftools.specifiers.InstrumentSpecifier(instrument=instrumenttools.Violin())
