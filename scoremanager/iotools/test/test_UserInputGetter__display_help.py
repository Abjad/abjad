# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter__display_help_01():
    r'''Question mark displays help.
    '''

    input_ = 'red~example~score m new ? q'
    score_manager._run(pending_input=input_)
    lines = [
        'Score manager - example scores',
        '> red example score',
        'Red Example Score (2013)',
        '> m',
        'Red Example Score (2013) - materials',
        '> new',
        'Enter material package name> ?',
        'Value  must be space-delimited lowercase string.',
        'Enter material package name> q',
        ]
    assert score_manager._transcript.first_lines == lines


def test_UserInputGetter__display_help_02():
    r'''Help string displays help.
    '''

    input_ = 'red~example~score m new help q'
    score_manager._run(pending_input=input_)
    lines = [
        'Score manager - example scores',
        '> red example score',
        'Red Example Score (2013)',
        '> m',
        'Red Example Score (2013) - materials',
        '> new',
        'Enter material package name> help',
        'Value  must be space-delimited lowercase string.',
        'Enter material package name> q',
        ]
    assert score_manager._transcript.first_lines == lines