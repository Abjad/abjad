# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_open_score_pdf_01():

    input_ = 'red~example~score spo q'
    score_manager._run(input_=input_)

    assert score_manager._session._attempted_to_open_file


def test_ScorePackageManager_open_score_pdf_02():

    input_ = 'blue~example~score spo q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    string =  "File ending in 'score.pdf' not found." in contents
    assert not score_manager._session._attempted_to_open_file