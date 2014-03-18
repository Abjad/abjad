# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ReservoirStartHelperCreationWizard__run_01():

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    input_ = 'q'
    assert wizard._run(pending_user_input=input_) == []

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    input_ = 'b'
    assert wizard._run(pending_user_input=input_) == []


def test_ReservoirStartHelperCreationWizard__run_02():

    wizard = scoremanager.wizards.ReservoirStartHelperCreationWizard()
    input_ = 'start~at~index~0'
    assert wizard._run(pending_user_input=input_) == \
        [('start at index 0', ())]
