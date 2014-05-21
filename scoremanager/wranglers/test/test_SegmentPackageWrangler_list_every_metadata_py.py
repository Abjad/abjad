# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_list_every_metadata_py_01():

    input_ = 'red~example~score g mdls* y q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    segments = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    paths = []
    for segment in segments:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            segment,
            '__metadata__.py',
            )
        paths.append(path)

    for path in paths:
        assert path in contents
    assert '3 __metadata__.py files found.' in contents


def test_SegmentPackageWrangler_list_every_metadata_py_02():

    input_ = 'g mdls* y q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    path = score_manager._configuration.example_score_packages_directory
    paths = [
        os.path.join(path, 'red_example_score'),
        ]
    for path in paths:
        assert path in contents
    assert '3 __metadata__.py files found.' in contents
