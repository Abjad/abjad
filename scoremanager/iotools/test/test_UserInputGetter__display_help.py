# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter__display_help_01():
    r'''Question mark displays help.
    '''

    input_ = 'red~example~score m new ? q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string  = 'Value  must be space-delimited lowercase string.'
    assert string in contents


def test_UserInputGetter__display_help_02():
    r'''Help string displays help.
    '''

    input_ = 'red~example~score m new help q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    string = 'Value  must be space-delimited lowercase string.'
    assert string in contents