# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_display_available_commands_01():
    
    input_ = '? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Score Manager - scores - available commands' in contents