# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_rename_package_01():
    r'''Creates package. Renames package.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_material',
        )
    new_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'new_test_material',
        )

    with systemtools.FilesystemState(remove=[path, new_path]):
        input_ = 'red~example~score m new test~material q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        input_ = 'red~example~score m ren test~material new_test_material y q'
        score_manager._run(input_=input_)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)