# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_make_package_01():
    r'''Makes segment package.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_04',
        )
    directory_entries = [
        '__make__.py',
        'definition.py',
        ]

    assert not os.path.exists(path)
    try:
        input_ = 'red~example~score g new segment~04 q'
        score_manager._run(pending_user_input=input_)
        assert os.path.exists(path)
        session = scoremanager.core.Session(is_test=True)
        manager = scoremanager.managers.SegmentPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
    finally:
        if os.path.exists(path):
            shutil.rmtree(path)
    assert not os.path.exists(path)