# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler__run_01():
    r'''Quit works.
    '''

    input_ = 'q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (2,)


def test_ScorePackageWrangler__run_02():
    r'''Home works.
    '''

    input_ = 'h q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))


def test_ScorePackageWrangler__run_03():
    r'''Junk is ignored.
    '''

    input_ = 'foo q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))


def test_ScorePackageWrangler__run_04():
    r'''Score is ignored.
    '''

    input_ = 's q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))


def test_ScorePackageWrangler__run_05():
    r'''Back works.
    '''

    input_ = 'b q'
    score_manager._run(pending_user_input=input_)
    assert score_manager._transcript.signature == (4, (0, 2))