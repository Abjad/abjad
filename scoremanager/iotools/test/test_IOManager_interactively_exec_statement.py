# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_interactively_exec_statement_01():

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='pyi 2**30 q')

    assert score_manager.session.io_transcript[1][1] == ['> pyi', '']
    assert score_manager.session.io_transcript[2][1] == ['>>> 2**30']
    assert score_manager.session.io_transcript[3][1] == ['1073741824', '']
    assert score_manager.session.io_transcript[4][1] == ['> q', '']


def test_IOManager_interactively_exec_statement_02():
    r'''Protects against senseless input.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='pyi foo q')

    assert score_manager.session.io_transcript[1][1] == ['> pyi', '']
    assert score_manager.session.io_transcript[2][1] == ['>>> foo']
    entry = ['Expression not executable.', '']
    assert score_manager.session.io_transcript[3][1] == entry
    assert score_manager.session.io_transcript[4][1] == ['> q', '']
