# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_open_every_score_pdf_01():

    input_ = 'so* y q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    assert 'Will open ...' in contents
    assert ide._session._attempted_to_open_file