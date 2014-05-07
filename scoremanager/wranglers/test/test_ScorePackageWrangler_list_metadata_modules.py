# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_list_metadata_modules_01():

    input_ = 'mdmls default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    path = score_manager._configuration.example_score_packages_directory_path
    paths = [
        os.path.join(path, 'blue_example_score'),
        os.path.join(path, 'etude_example_score'),
        os.path.join(path, 'red_example_score'),
        ]
    for path in paths:
        assert path in contents

    assert 'metadata modules found.' in contents