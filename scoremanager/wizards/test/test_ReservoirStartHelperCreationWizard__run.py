# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ReservoirStartHelperCreationWizard__run_01():

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    assert wizard._run(pending_user_input='q') == []

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    assert wizard._run(pending_user_input='b') == []


def test_ReservoirStartHelperCreationWizard__run_02():

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    assert wizard._run(pending_user_input='start~at~index~0') == \
        [('start at index 0', ())]
