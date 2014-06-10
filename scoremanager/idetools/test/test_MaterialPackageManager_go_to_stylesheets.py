# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_go_to_stylesheets_01():

    input_ = 'red~example~score m tempo~inventory y q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory (OAE)',
        'Red Example Score (2013) - stylesheets',
        ]
    assert score_manager._transcript.titles == titles