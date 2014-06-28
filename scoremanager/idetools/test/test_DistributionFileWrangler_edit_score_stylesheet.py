# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_DistributionFileWrangler_edit_score_stylesheet_01():

    input_ = 'red~example~score d sse q'
    ide._run(input_=input_)

    assert ide._session._attempted_to_open_file