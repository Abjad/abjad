# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_previous_score_01():

    input_ = 'red~example~score u << q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Étude Example Score (2013)',
        ]
    assert ide._transcript.titles == titles


def test_BuildFileWrangler_go_to_previous_score_02():

    input_ = 'uu << q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Red Example Score (2013)',
        ]
    assert ide._transcript.titles == titles