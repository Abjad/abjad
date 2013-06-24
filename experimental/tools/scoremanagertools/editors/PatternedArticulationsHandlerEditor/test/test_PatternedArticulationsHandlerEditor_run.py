from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_PatternedArticulationsHandlerEditor_run_01():

    editor = scoremanagertools.editors.PatternedArticulationsHandlerEditor()
    editor._run(pending_user_input="1 [['.', '^'], ['.']] (1, 16) (1, 8) cs'' c''' done", is_autoadvancing=True)


    handler = handlertools.PatternedArticulationsHandler(
        articulation_lists=[['.', '^'], ['.']],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=pitchtools.NamedChromaticPitch("cs''"),
        maximum_written_pitch=pitchtools.NamedChromaticPitch("c'''"))

    assert editor.target == handler
