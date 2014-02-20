# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageManager__run_01():
    r'''Global materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm sargasso q')
    assert score_manager.session.io_transcript.signature == (6,)

    score_manager._run(pending_user_input='lmm sargasso b q')
    assert score_manager.session.io_transcript.signature == (8, (2, 6))

    score_manager._run(pending_user_input='lmm sargasso h q')
    assert score_manager.session.io_transcript.signature == (8, (0, 6))

    score_manager._run(pending_user_input='lmm sargasso s q')
    assert score_manager.session.io_transcript.signature == (8, (4, 6))

    score_manager._run(pending_user_input='lmm sargasso foo q')
    assert score_manager.session.io_transcript.signature == (8, (4, 6))


def test_MaterialPackageManager__run_02():
    r'''Global materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='lmm sargasso q')
    string = 'Score manager - material library - sargasso multipliers'
    assert score_manager.session.io_transcript.last_menu_lines[0] == string


def test_MaterialPackageManager__run_03():
    r'''Score materials: quit, back, home, score & junk all work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (8,)

    string = 'red~example~score m tempo~inventory b q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (4, 8))

    string = 'red~example~score m tempo~inventory h q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (0, 8))

    string = 'red~example~score m tempo~inventory s q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (2, 8))

    string = 'red~example~score m tempo~inventory foo q'
    score_manager._run(pending_user_input=string)
    assert score_manager.session.io_transcript.signature == (10, (6, 8))


def test_MaterialPackageManager__run_04():
    r'''Score materials: breadcrumbs work.
    '''

    score_manager = scoremanager.core.ScoreManager()
    string = 'red~example~score m tempo~inventory q'
    score_manager._run(pending_user_input=string)
    string = 'Red Example Score (2013) - materials - tempo inventory'
    assert score_manager.session.io_transcript.last_menu_lines[0] == string
