# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_Getter_go_to_current_score_01():

    ide = scoremanager.idetools.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory da 1 d s q'
    ide._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - materials directory - tempo inventory (EDIT)',
        'Red Example Score (2013) - materials directory - tempo inventory - tempo (EDIT)',
        'Red Example Score (2013)',
        ]
    assert ide._transcript.titles == titles