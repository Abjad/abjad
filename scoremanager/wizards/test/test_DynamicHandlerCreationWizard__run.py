# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_DynamicHandlerCreationWizard__run_01():

    wizard = scoremanager.wizards.DynamicHandlerCreationWizard()
    wizard._run(pending_user_input='reiterateddynamic f (1, 16) done')

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    assert wizard.target == handler
