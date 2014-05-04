# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_edit_initializers_01():

    input_ = 'red~example~score m ine y q'
    score_manager._run(pending_user_input=input_)
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
            score_manager._configuration.example_score_packages_directory_path,
            'red_example_score',
            'materials',
            package_name,
            '__init__.py',
            )

    lines = []
    lines.append('Will edit ...')
    lines.extend(paths)

    for line in lines:
        assert line in contents