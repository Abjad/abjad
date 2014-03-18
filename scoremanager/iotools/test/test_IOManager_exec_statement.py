# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_IOManager_exec_statement_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'pyi 2**30 q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._transcript[1].lines == ['> pyi', '']
    assert score_manager._transcript[2].lines == ['>>> 2**30']
    assert score_manager._transcript[3].lines == ['1073741824', '']
    assert score_manager._transcript[4].lines == ['> q', '']


def test_IOManager_exec_statement_02():
    r'''Protects against senseless input.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'pyi foo q'
    score_manager._run(pending_user_input=input_)

    assert score_manager._transcript[1].lines == ['> pyi', '']
    assert score_manager._transcript[2].lines == ['>>> foo']
    entry = ['Expression not executable.', '']
    assert score_manager._transcript[3].lines == entry
    assert score_manager._transcript[4].lines == ['> q', '']
