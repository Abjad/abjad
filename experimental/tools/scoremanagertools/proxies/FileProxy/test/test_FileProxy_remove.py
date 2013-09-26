# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_FileProxy_remove_01():
    r'''Nonversioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_proxy.remove()
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)


def test_FileProxy_remove_02():
    r'''Versioned file.
    '''

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_proxy.make_empty_asset()
        assert os.path.exists(filesystem_path)
        file_proxy.repository_add()
        assert file_proxy.is_versioned()
        file_proxy.remove()
        assert not os.path.exists(filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
