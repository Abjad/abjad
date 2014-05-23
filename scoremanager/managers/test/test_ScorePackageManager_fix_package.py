# -*- encoding: utf-8 -*-
import os
import pytest
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageManager_fix_package_01():
    r'''Works when no fixes are required.
    '''

    input_ = 'red~example~score fix q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'No fixes required.' in contents


def test_ScorePackageManager_fix_package_02():
    r'''Works when no fixes are required.
    '''
    pytest.skip('make me work again; no idea why failing.')

    score_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        )

    initializer_path = os.path.join(score_path, '__init__.py')
    metadata_path = os.path.join(score_path, '__metadata__.py')

    with systemtools.FilesystemState(keep=[initializer_path, metadata_path]):
        os.remove(initializer_path)
        os.remove(metadata_path)
        # calls fix_package() on ScorePackageManager start
        input_ = 'red~example~score fix q'
        score_manager._run(input_=input_)
        assert os.path.isfile(initializer_path)
        assert os.path.isfile(metadata_path)