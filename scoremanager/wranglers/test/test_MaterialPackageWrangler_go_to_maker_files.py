# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_go_to_maker_files_01():
    r'''From materials directory to makers directory.
    '''

    input_ = 'red~example~score m k q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - maker modules',
        ]
    assert score_manager._transcript.titles == titles