# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_RegistrationComponent_autoedit_01():
    r'''Edits registration component source and target.
    '''

    target = pitchtools.RegistrationComponent()
    session = scoremanager.idetools.Session(is_test=True)
    autoeditor = scoremanager.idetools.Autoeditor(
        session=session,
        target=target,
        )
    input_ = 'source [A0, C8] target -18 q'
    autoeditor._session._pending_input = input_
    autoeditor._run()

    component = pitchtools.RegistrationComponent('[A0, C8]', -18)
    assert autoeditor.target == component