# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Session_command_history_string_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    ide._session._allow_unknown_command_during_test = True
    input_ = 'foo bar blah q'
    ide._run(input_=input_)
    assert ide._session.command_history_string == input_