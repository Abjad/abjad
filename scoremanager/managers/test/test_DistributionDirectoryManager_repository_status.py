# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_DistributionDirectoryManager_repository_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score d rst default q'
    score_manager._run(pending_user_input=input_)
    string = '# On branch master'

    assert string in score_manager._transcript.titles


def test_DistributionDirectoryManager_repository_status_02():
    r'''Works with Subversion.
    '''

    name = score_manager._find_svn_score_name()
    if not name:
        return

    input_ = 'ssl {} d rst default q'.format(name)
    score_manager._run(pending_user_input=input_)
    string = 'Press return to continue.'

    assert string in score_manager._transcript.titles