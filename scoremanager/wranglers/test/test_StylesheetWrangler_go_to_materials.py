# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_StylesheetWrangler_go_to_materials_01():
    r'''Goes from score stylesheets to score materials.
    '''

    input_ = 'red~example~score y m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Red Example Score (2013)',
        'Red Example Score (2013) - stylesheets',
        'Red Example Score (2013) - materials',
        ]
    assert score_manager._transcript.titles == titles


def test_StylesheetWrangler_go_to_materials_02():
    r'''Goes from stylesheets library to material library.
    '''

    input_ = 'y m q'
    score_manager._run(pending_input=input_)
    titles = [
        'Score Manager - scores',
        'Score Manager - stylesheets',
        'Score Manager - materials',
        ]
    assert score_manager._transcript.titles == titles