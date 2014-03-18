# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_status_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    string = 'lmm rst default q'
    score_manager._run(pending_user_input=string)
    title = '# On branch master'

    assert title in score_manager._transcript.titles
