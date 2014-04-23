# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_edit_paper_dimensions_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        )

    try:
        input_ = 'red~example~score p paper~dimensions A4 q'
        score_manager._run(pending_user_input=input_)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._get_metadatum('paper_dimensions') == 'A4'
    finally:
        input_ = 'red~example~score p paper~dimensions 8.5~x~11~in q'
        score_manager._run(pending_user_input=input_)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.ScorePackageManager
        manager = manager(path=path, session=session)
        assert manager._get_metadatum('paper_dimensions') == '8.5 x 11 in'