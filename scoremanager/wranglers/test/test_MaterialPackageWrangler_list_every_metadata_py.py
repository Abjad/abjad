# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_list_every_metadata_py_01():

    input_ = 'red~example~score m mdo y q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents
    materials = [
        'instrumentation',
        'magic_numbers',
        'pitch_range_inventory',
        'tempo_inventory',
        'time_signatures',
        ]
    paths = []
    for material in materials:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            'red_example_score',
            'materials',
            material,
            '__metadata__.py',
            )
        paths.append(path)

    assert 'Will open ...' in contents
    for path in paths:
        assert path in contents
    assert score_manager._session._attempted_to_open_file


def test_MaterialPackageWrangler_list_every_metadata_py_02():

    input_ = 'm mdo y q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    path = score_manager._configuration.example_score_packages_directory
    paths = [
        os.path.join(path, 'red_example_score'),
        ]
    for path in paths:
        assert path in contents

    assert 'Will open ...' in contents
    assert score_manager._session._attempted_to_open_file