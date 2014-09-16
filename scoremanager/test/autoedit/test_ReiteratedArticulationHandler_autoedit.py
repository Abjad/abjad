# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools import handlertools
import scoremanager


def test_ReiteratedArticulationHandler_autoedit_01():
    r'''Edits reiterated articulation handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    session._is_autostarting = True
    target = handlertools.ReiteratedArticulationHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "['.', '^'] (1, 16) (1, 8) cs'' c''' done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        minimum_duration=Duration(1, 16),
        maximum_duration=Duration(1, 8),
        minimum_written_pitch=NamedPitch("cs''"),
        maximum_written_pitch=NamedPitch("c'''"),
        )

    assert autoeditor.target == handler


def test_ReiteratedArticulationHandler_autoedit_02():
    r'''Edits reiterated articulation handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    session._is_autostarting = True
    target = handlertools.ReiteratedArticulationHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "['.', '^'] None None None None done"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.ReiteratedArticulationHandler(
        articulation_list=['.', '^'],
        )

    assert autoeditor.target == handler