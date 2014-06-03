# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_rewrite_every_metadata_py_01():

    input_ = 'mdw* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    path = score_manager._configuration.example_score_packages_directory
    paths = [
        os.path.join(path, 'blue_example_score', '__metadata__.py'),
        os.path.join(path, 'etude_example_score', '__metadata__.py'),
        os.path.join(path, 'red_example_score', '__metadata__.py'),
        ]
    for path in paths:
        assert path in contents

    assert 'Will rewrite ...' in contents
    assert '__metadata__.py files rewritten.' in contents