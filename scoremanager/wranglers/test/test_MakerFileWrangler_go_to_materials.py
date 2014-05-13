# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerFileWrangler_go_to_materials_01():
    r'''From score maker files to score materials.
    '''

    input_ = 'red~example~score k m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - maker files',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_MakerFileWrangler_go_to_materials_02():
    r'''From maker file library to material library.
    '''

    input_ = 'k m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score manager - example scores',
        'Score manager - maker files',
        'Score manager - materials',
        ]
    assert score_manager._transcript.titles == titles