import os
from experimental import *


def test_FileProxy_interactively_rename_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'test_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        assert not file_proxy.is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_test_file.txt')
        file_proxy.interactively_rename(pending_user_input='new_test_file.txt y q')
        assert file_proxy.filesystem_path == new_filesystem_path
        assert not os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
    finally:
        file_proxy.remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)


def test_FileProxy_interactively_rename_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'test_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_proxy.svn_add()
        assert file_proxy.is_versioned()
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_test_file.txt')
        file_proxy.interactively_rename(pending_user_input='new_test_file.txt y q')
        assert file_proxy.filesystem_path == new_filesystem_path
        assert os.path.exists(new_filesystem_path)
    finally:
        file_proxy.remove()
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
