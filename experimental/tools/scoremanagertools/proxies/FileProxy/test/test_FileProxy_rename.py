import os
from experimental import *


def test_FileProxy_rename_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(path_name=path)
    assert not os.path.exists(path)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path)
        assert not file_proxy.is_versioned
        new_path = os.path.join(
            score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'new_temporary_file.txt')
        file_proxy.rename(new_path)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
        file_proxy.remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)


def test_FileProxy_rename_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(path_name=path)
    assert not os.path.exists(path)

    try:
        file_proxy.conditionally_make_empty_asset()
        assert os.path.exists(path)
        file_proxy.svn_add()
        assert file_proxy.is_versioned
        new_path = os.path.join(
            score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'new_temporary_file.txt')
        file_proxy.rename(new_path)
        assert os.path.exists(new_path)
        assert file_proxy.path_name == new_path
    finally:
        file_proxy.remove()
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)
