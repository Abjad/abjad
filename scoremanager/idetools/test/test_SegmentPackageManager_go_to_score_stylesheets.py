# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageManager_go_to_score_stylesheets_01():

    input_ = 'red~example~score g A y q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments',
        'Red Example Score (2013) - segments - A',
        'Red Example Score (2013) - stylesheets',
        ]
    assert ide._transcript.titles == titles