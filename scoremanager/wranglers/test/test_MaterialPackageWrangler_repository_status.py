# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_MaterialPackageWrangler_repository_status_01():
    r'''Work with Git outside of score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'm rst q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents


def test_MaterialPackageWrangler_repository_status_02():
    r'''Work with Git inside score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    input_ = 'red~example~score m rst q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    assert 'On branch master' in contents


def test_MaterialPackageWrangler_repository_status_03():
    r'''Work with Subversion outside of score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=False)
    if not manager:
        return

    manager.repository_status()
    titles = manager._transcript.titles

    assert titles[0].endswith('...')
    assert len(titles) == 1


def test_MaterialPackageWrangler_repository_status_04():
    r'''Work with Subversion inside score.
    '''

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    wrangler = score_manager._material_package_wrangler
    manager = wrangler._find_svn_manager(inside_score=True)
    if not manager:
        return

    manager.repository_status()
    titles = manager._transcript.titles

    assert titles[0].endswith('...')
    assert len(titles) == 1