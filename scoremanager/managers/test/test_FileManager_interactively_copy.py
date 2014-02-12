# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager_interactively_copy_01():

    score_manager_configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_manager = scoremanager.managers.FileManager(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(filesystem_path)
        new_filesystem_path = os.path.join(
            score_manager_configuration.score_manager_tools_directory_path, 'new_temporary_file.txt')
        file_manager.interactively_copy(pending_user_input='new_temporary_file.txt y q')
        assert os.path.exists(filesystem_path)
        assert os.path.exists(new_filesystem_path)
        file_manager._remove()
        os.remove(new_filesystem_path)
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        if os.path.exists(new_filesystem_path):
            os.remove(new_filesystem_path)
        assert not os.path.exists(filesystem_path)
        assert not os.path.exists(new_filesystem_path)
