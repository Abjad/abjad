# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_ScorePackageWrangler_rewrite_metadata_modules_01():

    input_ = 'mdmrw default q'
    score_manager._run(pending_user_input=input_)
    contents = score_manager._transcript.contents

    path = score_manager._configuration.example_score_packages_directory_path
    paths = [
        os.path.join(path, 'blue_example_score', '__metadata__.py'),
        os.path.join(path, 'etude_example_score', '__metadata__.py'),
        os.path.join(path, 'red_example_score', '__metadata__.py'),
        ]
    for path in paths:
        assert path in contents

    assert 'Rewriting' in contents
    assert 'metadata modules rewritten.' in contents