# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_go_to_all_scores_01():

    input_ = 'red~example~score k S q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores depot',
        'Red Example Score (2013)',
        'Red Example Score (2013) - makers directory',
        'Abjad IDE - scores depot',
        ]
    assert ide._transcript.titles == titles


def test_MakerFileWrangler_go_to_all_scores_02():

    input_ = 'K S q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores depot',
        'Abjad IDE - makers depot',
        'Abjad IDE - scores depot',
        ]
    assert ide._transcript.titles == titles