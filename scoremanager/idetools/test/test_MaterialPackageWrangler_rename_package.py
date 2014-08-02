# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_rename_package_01():
    r'''Creates package. Renames package.
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_material',
        )
    new_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'new_test_material',
        )

    with systemtools.FilesystemState(remove=[path, new_path]):
        input_ = 'red~example~score m new test~material y q'
        ide._run(input_=input_)
        assert os.path.exists(path)
        input_ = 'red~example~score m ren test~material new~test~material y q'
        ide._run(input_=input_)
        assert not os.path.exists(path)
        assert os.path.exists(new_path)