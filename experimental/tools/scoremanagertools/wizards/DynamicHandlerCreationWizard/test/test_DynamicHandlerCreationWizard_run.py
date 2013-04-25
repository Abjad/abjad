from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_DynamicHandlerCreationWizard_run_01():

    wizard = scoremanagertools.wizards.DynamicHandlerCreationWizard()
    wizard.run(user_input='reiterateddynamic f (1, 16) done')

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 16),
        )

    assert wizard.target == handler
