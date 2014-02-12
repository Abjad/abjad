# -*- encoding: utf-8 -*-
from experimental import *


def test_ArticulationHandlerCreationWizard_run_01():

    wizard = scoremanager.wizards.ArticulationHandlerCreationWizard()
    wizard._run(
        pending_user_input="reit ['^', '.'] (1, 64) (1, 4) c c'''' done"
        )

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=NamedPitch('c'),
        maximum_written_pitch=NamedPitch("c''''"),
        )

    assert wizard.target == handler
