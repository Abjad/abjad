# -*- encoding: utf-8 -*-
import os
import pytest
pytest.skip()
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildDirectoryManager_commit_to_repository_01():

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.BuildDirectoryManager,
        repository='git',
        system=True,
        )

    manager._session._is_repository_test = True
    manager.commit_to_repository(prompt=False)
    assert manager._session._attempted_to_commit_to_repository
    

def test_BuildDirectoryManager_commit_to_repository_02():

    manager = score_manager._find_up_to_date_manager(
        scoremanager.managers.BuildDirectoryManager,
        repository='svn',
        system=False,
        )
            
    if not manager:
        return

    manager._session._is_repository_test = True
    manager.commit_to_repository(prompt=False)
    assert manager._session._attempted_to_commit_to_repository