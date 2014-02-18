# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_ScoreManager_01():
    r'''Main menu to mothballed scores.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='mb q')
    score_manager.session.io_transcript.signature == (4,)


def test_ScoreManager_02():
    r'''Main menu header is the same even after state change to secondary menu.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='q')
    string = 'Score manager - active scores'
    assert score_manager.session.io_transcript[-2][1][0] == string


def test_ScoreManager_03():
    r'''Junk works.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='foo q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))

    score_manager._run(pending_user_input='foo bar q')
    assert score_manager.session.io_transcript.signature == (6, (0, 2, 4))


def test_ScoreManager_04():
    r'''Back is handled correctly.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='b q')
    assert score_manager.session.io_transcript.signature == (4, (0, 2))


def test_ScoreManager_05():
    r'''Python prompt works.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='ppi 2**30 q')

    assert score_manager.session.io_transcript[1][1] == ['> ppi', '']
    assert score_manager.session.io_transcript[2][1] == ['>>> 2**30']
    assert score_manager.session.io_transcript[3][1] == ['1073741824', '']
    assert score_manager.session.io_transcript[4][1] == ['> q', '']


def test_ScoreManager_06():
    r'''Python prompt protects against senseless input.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='ppi foo q')

    assert score_manager.session.io_transcript[1][1] == ['> ppi', '']
    assert score_manager.session.io_transcript[2][1] == ['>>> foo']
    entry = ['Expression not executable.', '']
    assert score_manager.session.io_transcript[3][1] == entry
    assert score_manager.session.io_transcript[4][1] == ['> q', '']


def test_ScoreManager_07():
    r'''Shared session.
    '''

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager.score_package_wrangler

    assert score_manager.session is wrangler.session
