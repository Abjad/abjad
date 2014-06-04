# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_UserInputGetter_go_to_current_score_01():

    score_manager = scoremanager.core.AbjadIDE(is_test=True)
    input_ = 'red~example~score m tempo~inventory ae 1 d s q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013)',
        ]
    assert score_manager._transcript.titles == titles