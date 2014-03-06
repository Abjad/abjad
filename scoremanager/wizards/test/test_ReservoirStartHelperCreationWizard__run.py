# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ReservoirStartHelperCreationWizard__run_01():

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    assert wizard._run(pending_user_input='q', is_test=True) == []

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    assert wizard._run(pending_user_input='b', is_test=True) == []


def test_ReservoirStartHelperCreationWizard__run_02():

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    input_ = 'start~at~index~0'
    assert wizard._run(pending_user_input=input_, is_test=True) == \
        [('start at index 0', ())]
