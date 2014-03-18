# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialManager_view_illustration_pdf_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'lmm example~notes pdfv q'
    score_manager._run(pending_user_input=input_, is_test=True)
    titles = [
        'Score manager - example scores', 
        'Score manager - material library', 
        'Score manager - material library - example notes', 
        'Score manager - material library - example notes',
        ]

    assert score_manager._session.attempted_to_open_file
    assert score_manager._transcript.titles == titles
