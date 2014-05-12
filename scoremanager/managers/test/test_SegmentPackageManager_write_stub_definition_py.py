# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_write_stub_definition_py_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score g segment~01 dmws y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        assert not filecmp.cmp(path, path + '.backup')