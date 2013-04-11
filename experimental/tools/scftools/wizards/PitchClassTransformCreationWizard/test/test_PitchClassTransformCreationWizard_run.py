from experimental import *


def test_PitchClassTransformCreationWizard_run_01():

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='q') == []

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='b') == []


def test_PitchClassTransformCreationWizard_run_02():

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='transpose q') == []

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='transpose b q') == []

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='invert q') == [('invert', ())]

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='invert b') == [('invert', ())]

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='multiply q') == []

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='multiply b q') == []


def test_PitchClassTransformCreationWizard_run_03():

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='transpose 1 q') == [('transpose', (1,))]

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='multiply 5 q') == [('multiply', (5,))]

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='transpose 1 multiply 5 q') == [
        ('transpose', (1,)), ('multiply', (5,))]

    wizard = scftools.wizards.PitchClassTransformCreationWizard()
    assert wizard.run(user_input='transpose 1 invert multiply 5 q') == [
        ('transpose', (1,)), ('invert', ()), ('multiply', (5,))]
