# -*- encoding: utf-8 -*-
from experimental import *


def test_PerformerCreationWizard_make_performer_configuration_menu_01():
    r'''Clarinetist configuration menu contains exactly one default entry.
    '''

    score_manager = scoremanagertools.scoremanager.ScoreManager()
    score_manager._run(pending_user_input=
        'red~example~score score~setup performers add clarinetist q')
    last_menu_lines = score_manager.session.io_transcript.last_menu_lines

    end = 'clarinet in B-flat (default)'
    assert len([x for x in last_menu_lines if x.endswith(end)]) == 1
