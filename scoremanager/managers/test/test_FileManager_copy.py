# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager_copy_01():

    score_manager_configuration = scoremanager.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        path=path,
        )
    assert not os.path.exists(path)

    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        new_path = os.path.join(
            score_manager_configuration.score_manager_directory_path, 
            'new_temporary_file.txt',
            )
        string = 'new_temporary_file.txt y q'
        file_manager.copy(pending_user_input=string)
        assert os.path.exists(path)
        assert os.path.exists(new_path)
        file_manager._remove()
        os.remove(new_path)
    finally:
        if os.path.exists(path):
            os.remove(path)
        if os.path.exists(new_path):
            os.remove(new_path)
        assert not os.path.exists(path)
        assert not os.path.exists(new_path)
