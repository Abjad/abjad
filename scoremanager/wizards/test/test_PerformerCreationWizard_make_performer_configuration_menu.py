# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_PerformerCreationWizard_make_performer_configuration_menu_01():
    r'''Clarinetist configuration menu contains exactly one default entry.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score setup instrumentation add clarinetist q'
    score_manager._run(pending_user_input=string)
    last_menu_lines = score_manager._session.transcript.last_menu_lines

    end = 'clarinet in B-flat (default)'
    assert len([x for x in last_menu_lines if x.endswith(end)]) == 1
