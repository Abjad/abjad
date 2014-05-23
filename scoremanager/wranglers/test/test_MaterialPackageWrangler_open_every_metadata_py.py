# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_open_every_metadata_py_01():

    input_ = 'red~example~score m mdo* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert score_manager._session._attempted_to_open_file

    package_names = (
        'instrumentation',
        'magic_numbers',
        'pitch_range_inventory',
        'tempo_inventory',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            package_name,
            '__metadata__.py',
            )

    lines = []
    lines.append('Will open ...')
    lines.extend(paths)

    for line in lines:
        assert line in contents