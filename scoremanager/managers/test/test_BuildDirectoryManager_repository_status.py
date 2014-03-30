# -*- encoding: utf-8 -*-
import pytest
pytest.skip()
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildDirectoryManager_repository_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score u rst default q'
    score_manager._run(pending_user_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_BuildDirectoryManager_repository_status_02():
    r'''Works with Subversion.
    '''

    name = score_manager._find_svn_score_name()
    if not name:
        return

    input_ = 'ssl {} u rst default q'.format(name)
    score_manager._run(pending_user_input=input_)
    string = 'Press return to continue.'

    assert string in score_manager._transcript.titles