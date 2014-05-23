# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_SegmentPackageWrangler_open_every_metadata_py_01():

    input_ = 'red~example~score g mdo* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert score_manager._session._attempted_to_open_file

    package_names = (
        'segment_01',
        'segment_02',
        'segment_03',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'segments',
            package_name,
            '__metadata__.py',
            )

    lines = []
    lines.append('Will open ...')
    lines.extend(paths)

    for line in lines:
        assert line in contents