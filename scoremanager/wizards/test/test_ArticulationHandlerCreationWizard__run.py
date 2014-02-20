# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_ArticulationHandlerCreationWizard__run_01():

    wizard = scoremanager.wizards.ArticulationHandlerCreationWizard()
    string = "reit ['^', '.'] (1, 64) (1, 4) c c'''' done"
    wizard._run(pending_user_input=string)

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=NamedPitch('c'),
        maximum_written_pitch=NamedPitch("c''''"),
        )

    assert wizard.target == handler
