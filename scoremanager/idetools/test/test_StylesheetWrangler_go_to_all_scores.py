# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_StylesheetWrangler_go_to_all_scores_01():

    input_ = 'red~example~score y ss q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets directory',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles


def test_StylesheetWrangler_go_to_all_scores_02():

    input_ = 'yy ss q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - stylesheets depot',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles