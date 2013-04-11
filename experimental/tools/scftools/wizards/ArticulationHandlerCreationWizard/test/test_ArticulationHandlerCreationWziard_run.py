from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_ArticulationHandlerCreationWziard_run_01():

    wizard = scftools.wizards.ArticulationHandlerCreationWizard()
    wizard.run(user_input="reit ['^', '.'] (1, 64) (1, 4) c c'''' done")

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['^', '.'],
        minimum_duration=Duration(1, 64),
        maximum_duration=Duration(1, 4),
        minimum_written_pitch=pitchtools.NamedChromaticPitch('c'),
        maximum_written_pitch=pitchtools.NamedChromaticPitch("c''''"),
        )

    assert wizard.target == handler
