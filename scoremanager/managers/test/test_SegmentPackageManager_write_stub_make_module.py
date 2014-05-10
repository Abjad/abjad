# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageManager_write_stub_make_module_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'segments',
        'segment_01',
        '__make__.py',
        )

    with systemtools.AssetState(keep=[path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score g segment~01 mmws y q'
        score_manager._run(pending_input=input_)
        assert os.path.isfile(path)
        contents = score_manager._transcript.contents
        assert 'Will write stub to' in contents
        assert 'Wrote stub to' in contents