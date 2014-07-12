# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_go_back_01():

    input_ = 'red~example~score b q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Abjad IDE - scores',
        ]
    assert ide._transcript.titles == titles