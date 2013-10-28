# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import handlertools
from experimental import *
import py.test


@py.test.skip('FIXME: Broken by class package flattening.')
def test_DynamicHandlerCreationWizard_run_01():

    wizard = scoremanagertools.wizards.DynamicHandlerCreationWizard()
    wizard._run(pending_user_input='reiterateddynamic f (1, 16) done')

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    assert wizard.target == handler
