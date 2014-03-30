# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_Editor___repr___01():

    input_ = 'red~example~score p instr cellist cello sdv default q'
    score_manager._run(pending_user_input=input_)
    transcript_contents = score_manager._transcript.contents
    
    string = '<InstrumentationEditor(target=InstrumentationSpecifier)>'
    assert string in transcript_contents

    string = '<PerformerEditor(target=Performer)>'
    assert string in transcript_contents

    string = '<InstrumentEditor(target=Cello)>' 
    assert string in transcript_contents