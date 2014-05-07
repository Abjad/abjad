# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_write_stub_initializer_01():
    r'''Works when initializer doesn't already exist.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        '__init__.py',
        )

    assert not os.path.isfile(path)

    try:
        input_ = 'red~example~score g segment~01 inws y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        contents = score_manager._transcript.contents
        assert 'Will write stub to' in contents
        assert 'Wrote stub to' in contents
    finally:
        if os.path.exists(path):
            os.remove(path)

    assert not os.path.isfile(path)