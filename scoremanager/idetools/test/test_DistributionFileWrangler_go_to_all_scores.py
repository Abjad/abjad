# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_go_to_all_scores_01():

    input_ = 'red~example~score d S q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - distribution files',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles


def test_DistributionFileWrangler_go_to_all_scores_02():

    input_ = 'd S q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - distribution files',
        'Abjad IDE - scores',
        ]
    assert score_manager._transcript.titles == titles