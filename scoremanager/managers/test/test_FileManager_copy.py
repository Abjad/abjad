# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_FileManager_copy_01():

    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path, 
        'new_temporary_file.txt',
        )
    session = scoremanager.core.Session()
    file_manager = scoremanager.managers.FileManager(
        path=path,
        session=session,
        )
    input_ = 'new_temporary_file.txt y q'

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        file_manager.copy(pending_user_input=input_)
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
