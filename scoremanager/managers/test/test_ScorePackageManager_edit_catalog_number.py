# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_edit_catalog_number_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        )

    manager = scoremanager.managers.ScorePackageManager
    manager = manager(path=path, session=score_manager._session)
    assert manager._get_metadatum('catalog_number') == '#165'

    try:
        input_ = 'red~example~score p catalog~number for~foo~bar q'
        score_manager._run(pending_user_input=input_)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._get_metadatum('catalog_number') == 'for foo bar'
    finally:
        input_ = 'red~example~score p catalog~number #165 q'
        score_manager._run(pending_user_input=input_)

    assert manager._get_metadatum('catalog_number') == '#165'