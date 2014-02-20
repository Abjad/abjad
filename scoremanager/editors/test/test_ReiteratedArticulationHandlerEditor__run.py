# -*- encoding: utf-8 -*-
from abjad import *
from experimental import *
import scoremanager


def test_ReiteratedArticulationHandlerEditor__run_01():

    editor = scoremanager.editors.ReiteratedArticulationHandlerEditor()
    string = "['.', '^'] (1, 16) (1, 8) cs'' c''' done"
    editor._run(
        pending_user_input=string, 
        is_autoadvancing=True, 
        is_autostarting=True,
        )

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=NamedPitch("cs''"),
        maximum_written_pitch=NamedPitch("c'''"),
        )

    assert editor.target == handler


def test_ReiteratedArticulationHandlerEditor__run_02():

    editor = scoremanager.editors.ReiteratedArticulationHandlerEditor()
    string = "['.', '^'] None None None None done"
    editor._run(
        pending_user_input=string,
        is_autoadvancing=True, 
        is_autostarting=True,
        )

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        )

    assert editor.target == handler
