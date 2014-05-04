# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageManager_configure_autoeditor_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'test_tempo_inventory',
        )

    assert not os.path.exists(path)

    try:
        input_ = 'red~example~score m new test~tempo~inventory'
        input_ += ' pca TempoInventory default q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        string = 'Package configured for TempoInventory autoeditor.'
        assert string in contents
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)

    assert not os.path.exists(path)