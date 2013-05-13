import os
from experimental import *


def test_FileProxy_remove_interactively_01():
    '''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_proxy.remove_interactively(user_input='remove default q')
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)


def test_FileProxy_remove_interactively_02():
    '''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_proxy.svn_add()
        assert file_proxy.is_versioned
        file_proxy.remove_interactively(user_input='remove default q')
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
