# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerCreationWizard__run_01():

    wizard = scoremanager.wizards.DynamicHandlerCreationWizard()
    input_ = 'reiterateddynamic f (1, 16) done'
    wizard._run(pending_user_input=input_, is_test=True)

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    assert wizard.target == handler
