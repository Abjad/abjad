# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_go_to_distribution_files_01():
    r'''From materials directory to distribution directory.
    '''

    input_ = 'red~example~score m d q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials',
        'Red Example Score (2013) - distribution files',
        ]
    assert score_manager._transcript.titles == titles