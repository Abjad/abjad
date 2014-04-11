# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)
configuration = score_manager._configuration


def test_ScorePackageWrangler_list_storehouses_01():

    input_ = 'hls q'
    score_manager._run(pending_user_input=input_)

    path = os.path.join(
        configuration.example_score_packages_directory_path,
        'red_example_score',
        )
    assert path in score_manager._transcript.contents

    path = os.path.join(
        configuration.example_score_packages_directory_path,
        'blue_example_score',
        )
    assert path in score_manager._transcript.contents

    path = os.path.join(
        configuration.example_score_packages_directory_path,
        'etude_example_score',
        )
    assert path in score_manager._transcript.contents