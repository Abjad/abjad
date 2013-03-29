import scf


def test_ReservoirStartHelperCreationWizard_run_01():

    wizard = scf.wizards.ReservoirStartHelperCreationWizard()
    assert wizard.run(user_input='q') == []

    wizard = scf.wizards.ReservoirStartHelperCreationWizard()
    assert wizard.run(user_input='b') == []


def test_ReservoirStartHelperCreationWizard_run_02():

    wizard = scf.wizards.ReservoirStartHelperCreationWizard()
    assert wizard.run(user_input='start~at~index~0') == [('start at index 0', ())]
