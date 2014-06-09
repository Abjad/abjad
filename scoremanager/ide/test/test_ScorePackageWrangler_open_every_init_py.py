# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_open_every_init_py_01():

    input_ = 'no* y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    assert 'Will open ...' in contents

    package_names = (
        'blue_example_score',
        'etude_example_score',
        'red_example_score',
        )

    paths = []
    for package_name in package_names:
        path = os.path.join(
            score_manager._configuration.example_score_packages_directory,
            package_name,
            '__init__.py',
            )

    for path in paths:
        assert path in contents

    assert score_manager._session._attempted_to_open_file