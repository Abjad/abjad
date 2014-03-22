# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_ScorePackageManager_repository_status_01():
    r'''Works with Git.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score rst default q'
    score_manager._run(pending_user_input=input_)
    title = '# On branch master'

    assert title in score_manager._transcript.titles


def test_ScorePackageManager_repository_status_02():
    r'''Works with Subversion.
    '''

    session = scoremanager.core.Session(is_test=True)
    wrangler = scoremanager.wranglers.ScorePackageWrangler(session=session)
    manager = wrangler._find_up_to_date_versioned_manager(
        system=False,
        repository='svn',
        )

    if not manager:
        return

    manager.repository_status(prompt=False)
    line = '{} ...'.format(manager._package_path)
    titles = [
        line,
        '',
        ]

    assert manager._transcript.titles == titles