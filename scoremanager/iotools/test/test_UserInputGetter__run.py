# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter__run_01():
    r'''Entering junk during confirmation displays value reminder message.
    '''

    input_ = 'red~example~score u mc foo q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string = "Value for 'ok?' must be 'y' or 'n'."
    assert string in contents


def test_UserInputGetter__run_02():
    r'''Entering 'n' during confirmation cancels getter.
    '''

    input_ = 'red~example~score u mc n q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'Value for' not in contents


def test_UserInputGetter__run_03():
    r'''Entering 'N' during confirmation cancels getter.
    '''

    input_ = 'red~example~score u mc N q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'Value for' not in contents