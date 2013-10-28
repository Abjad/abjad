# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import handlertools
from experimental import *
import py.test


@py.test.skip('FIXME: Broken by class package flattening.')
def test_ArticulationHandlerCreationWziard_run_01():

    wizard = scoremanagertools.wizards.ArticulationHandlerCreationWizard()
    wizard._run(pending_user_input="reit ['^', '.'] (1, 64) (1, 4) c c'''' done")

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=pitchtools.NamedPitch('c'),
        maximum_written_pitch=pitchtools.NamedPitch("c''''"),
        )

    assert wizard.target == handler
