# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageManager_open_score_pdf_01():

    input_ = 'red~example~score so q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file


def test_ScorePackageManager_open_score_pdf_02():

    input_ = 'blue~example~score so q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    string =  "File ending in 'score.pdf' not found." in contents
    assert not ide._session._attempted_to_open_file