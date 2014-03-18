# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_StylesheetWrangler_remove_01():

    score_manager = scoremanager.core.ScoreManager(is_test=True)
    path = os.path.join(
        configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily',
        )
    backup_path = os.path.join(
        configuration.abjad_stylesheets_directory_path,
        'clean-letter-14.ily.backup',
        )

    assert os.path.exists(path)
    shutil.copyfile(path, backup_path)
    assert os.path.exists(backup_path)

    input_ = 'lmy rm clean-letter-14.ily remove q'
    score_manager._run(pending_user_input=input_)
    assert not os.path.exists(path)
    assert os.path.exists(backup_path)
    shutil.move(backup_path, path)
    manager = scoremanager.managers.FileManager(
        path=path,
        session=score_manager._session,
        )
    manager.add()

    assert os.path.exists(path)
    assert not os.path.exists(backup_path)
