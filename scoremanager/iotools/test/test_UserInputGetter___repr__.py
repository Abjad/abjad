# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_UserInputGetter___repr___01():

    input_ = 'étude~example~score p instr ps guitar nm sdv default q'
    score_manager._run(pending_user_input=input_)
    transcript_contents = score_manager._transcript.contents

    string = '<UserInputGetter (1)>'
    assert string in transcript_contents