# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_repository_status_01():
    r'''Works with Git.
    '''

    input_ = 'red~example~score rst q'
    score_manager._run(pending_user_input=input_)
    string = '# On branch master'

    assert string in score_manager._transcript.titles
    assert score_manager._session.proceed_count == 0


def test_ScorePackageManager_repository_status_02():
    r'''Works with Subversion.
    '''

    name = score_manager._score_package_wrangler._find_svn_score_name()
    if not name:
        return

    input_ = 'ssl {} rst q'.format(name)
    score_manager._run(pending_user_input=input_)
    string = '...'

    assert string in score_manager._transcript.contents
    assert score_manager._session.proceed_count == 0