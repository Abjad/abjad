# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_ScorePackageManager_add_01():

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
