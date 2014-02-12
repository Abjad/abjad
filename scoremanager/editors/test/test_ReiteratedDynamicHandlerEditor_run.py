# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_ReiteratedDynamicHandlerEditor_run_01():

    editor = scoremanager.editors.ReiteratedDynamicHandlerEditor()
    editor._run(pending_user_input="1 f Duration(1, 8) q", is_autoadvancing=True)

    handler = handlertools.ReiteratedDynamicHandler(
        dynamic_name='f',
        minimum_duration=Duration(1, 8),
        )

    assert editor.target == handler
