# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter_back_01():
    r'''Back works.
    '''

    input_ = 'red~example~score m tempo~inventory ae 1 d b q'
    score_manager._run(input_=input_)

    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory (AE)',
        'Red Example Score (2013) - materials - tempo inventory (AE) - tempo inventory',
        'Red Example Score (2013) - materials - tempo inventory (AE) - tempo inventory - tempo',
        'Red Example Score (2013) - materials - tempo inventory (AE) - tempo inventory - tempo',
        ]
    assert score_manager._transcript.titles == titles