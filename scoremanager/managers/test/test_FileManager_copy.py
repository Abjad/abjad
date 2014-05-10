# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_FileManager_copy_01():

    path = os.path.join(
        configuration.score_manager_directory_path,
        'temporary-file.txt',
        )
    new_path = os.path.join(
        configuration.score_manager_directory_path,
        'new-temporary-file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    file_manager = scoremanager.managers.FileManager(
        path=path,
        session=session,
        )

    with systemtools.FilesystemState(remove=[path, new_path]):
        file_manager._make_empty_asset()
        assert os.path.exists(path)
        input_ = 'new-temporary-file.txt y q'
        file_manager._session._pending_input = input_
        file_manager.copy()
        assert os.path.exists(path)
        assert os.path.exists(new_path)