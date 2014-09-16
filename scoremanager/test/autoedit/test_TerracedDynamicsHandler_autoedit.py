# -*- encoding: utf-8 -*-
import os
from abjad import *
from abjad.tools import handlertools
import scoremanager


def test_TerracedDynamicsHandler_autoedit_01():
    r'''Edits terraced dynamics handler.
    '''

    session = scoremanager.idetools.Session(is_test=True)
    session._autoadvance_depth = 1
    target = handlertools.TerracedDynamicsHandler()
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = "['p', 'f', 'f'] Duration(1, 8) q"
    autoeditor._session._pending_input = input_
    autoeditor._run()

    handler = handlertools.TerracedDynamicsHandler(
        dynamics=['p', 'f', 'f'],
        minimum_duration=Duration(1, 8),
        )

    assert autoeditor.target == handler