# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_rename_package_01():
    r'''Creates package. Renames package.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_04',
        )
    new_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'renamed_segment_04',
        )

    assert not os.path.exists(path)
    assert not os.path.exists(new_path)
    try:
        input_ = 'red~example~score g new segment~04 q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        input_ = 'red~example~score g ren segment~04 renamed_segment_04 y q'
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