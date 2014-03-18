# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ScorePackageManager_add_01():
    r'''Add two files to Subversioned-managed score package.
    '''

    path = configuration.user_score_packages_directory_path
    found_svn_versioned_score_package = False
    for directory_entry in os.listdir(path):
        directory_path = os.path.join(path, directory_entry)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ScorePackageManager(
            path=directory_path,
            session=session,
            )
        if manager._is_svn_versioned() and manager._is_up_to_date():
            found_svn_versioned_score_package = True
            break

    if not found_svn_versioned_score_package:
        return

    assert manager._is_up_to_date()
    path_1 = os.path.join(manager._path, 'tmp_1.py')
    path_2 = os.path.join(manager._path, 'tmp_2.py')

    assert not os.path.exists(path_1)
    assert not os.path.exists(path_2)
    try:
        with file(path_1, 'w') as file_pointer:
            file_pointer.write('')
        with file(path_2, 'w') as file_pointer:
            file_pointer.write('')
        assert os.path.exists(path_1)
        assert os.path.exists(path_2)
        assert not manager._is_up_to_date()
        assert manager._get_unadded_asset_paths() == [path_1, path_2]
        assert manager._get_added_asset_paths() == []
        manager.add()
        assert manager._get_unadded_asset_paths() == []
        assert manager._get_added_asset_paths() == [path_1, path_2]
        manager._unadd_added_assets(prompt=False)
        assert manager._get_unadded_asset_paths() == [path_1, path_2]
        assert manager._get_added_asset_paths() == []
        os.remove(path_1)
        os.remove(path_2)
    finally:
        if os.path.exists(path_1):
            os.remove(path_1)
        if os.path.exists(path_2):
            os.remove(path_2)
    assert not os.path.exists(path_1)
    assert not os.path.exists(path_2)
    assert manager._is_up_to_date()
