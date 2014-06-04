# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_BuildFileWrangler_go_to_distribution_files_01():
    r'''From build directory to distribution directory.
    '''

    input_ = 'red~example~score u d q'
    score_manager._run(input_=input_)
    titles = [
        'Abjad IDE - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build files',
        'Red Example Score (2013) - distribution files',
        ]
    assert score_manager._transcript.titles == titles