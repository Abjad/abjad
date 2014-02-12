# -*- encoding: utf-8 -*-
from experimental import *


def test_PatternedArticulationsHandlerEditor_run_01():

    editor = scoremanager.editors.PatternedArticulationsHandlerEditor()
    editor._run(pending_user_input="1 [['.', '^'], ['.']] (1, 16) (1, 8) cs'' c''' done", is_autoadvancing=True)


    handler = handlertools.PatternedArticulationsHandler(
        articulation_lists=[['.', '^'], ['.']],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=NamedPitch("cs''"),
        maximum_written_pitch=NamedPitch("c'''"))

    assert editor.target == handler
