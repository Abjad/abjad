# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_rename_package_01():
    r'''Creates material package. Renames material package.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'test_material',
        )
    new_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'materials',
        'new_test_material',
        )

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        input_ = 'red~example~score m new test~material q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        input_ = 'red~example~score m ren test~material new_test_material y q'
        score_manager._run(pending_user_input=input_)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
    assert not os.path.exists(path)
    assert not os.path.exists(new_path)