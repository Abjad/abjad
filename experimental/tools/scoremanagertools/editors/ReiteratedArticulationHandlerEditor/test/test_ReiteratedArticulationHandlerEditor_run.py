# -*- encoding: utf-8 -*-
from abjad import *
from experimental.tools import handlertools
from experimental import *


def test_ReiteratedArticulationHandlerEditor_run_01():

    editor = scoremanagertools.editors.ReiteratedArticulationHandlerEditor()
    editor._run(pending_user_input="['.', '^'] (1, 16) (1, 8) cs'' c''' done",
        is_autoadvancing=True, is_autostarting=True)

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=NamedPitch("cs''"),
        maximum_written_pitch=NamedPitch("c'''"),
        )

    assert editor.target == handler


def test_ReiteratedArticulationHandlerEditor_run_02():

    editor = scoremanagertools.editors.ReiteratedArticulationHandlerEditor()
    editor._run(pending_user_input="['.', '^'] None None None None done",
        is_autoadvancing=True, is_autostarting=True)

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        )

    assert editor.target == handler
