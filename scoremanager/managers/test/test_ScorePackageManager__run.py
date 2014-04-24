# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager__run_01():
    r'''Main menu looks like this.
    '''

    input_ = 'red~example~score q'
    score_manager._run(pending_user_input=input_)

    lines = [
        'Red Example Score (2013)',
        '',
        '      build (u)',
        '      distribution (d)',
        '      makers (k)',
        '      materials (m)',
        '      segments (g)',
        '      stylesheets (y)',
        '',
        '      score - open pdf (spo)',
        '',
        ]
    assert score_manager._transcript.last_menu_lines == lines


def test_ScorePackageManager__run_02():
    r'''Home works.
    '''

    input_ = 'red~example~score h q'
    score_manager._run(pending_user_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Score manager - example scores',
        ]
    assert score_manager._transcript.titles == titles


def test_ScorePackageManager__run_03():
    r'''User 'b' input returns home.
    '''

    input_ = 'red~example~score b q'
    score_manager._run(pending_user_input=input_)

    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Score manager - example scores',
        ]
    assert score_manager._transcript.titles == titles