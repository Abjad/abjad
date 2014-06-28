# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_go_to_all_scores_01():

    input_ = 'red~example~score g S q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles


def test_SegmentPackageWrangler_go_to_all_scores_02():

    input_ = 'G S q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - segments',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles