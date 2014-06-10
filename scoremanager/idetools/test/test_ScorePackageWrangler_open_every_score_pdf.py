# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_open_every_score_pdf_01():

    input_ = 'spo* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Will open ...' in contents
    assert score_manager._session._attempted_to_open_file