# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageManager_go_to_score_build_files_01():

    input_ = 'red~example~score m tempo~inventory u q'
    score_manager._run(input_=input_)

    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - materials - tempo inventory',
        'Red Example Score (2013) - build files',
        ]
    assert score_manager._transcript.titles == titles