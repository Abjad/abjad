# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MaterialPackageWrangler_rewrite_every_metadata_py_01():

    input_ = 'm mdrw default q'
    score_manager._run(pending_input=input_)
    contents = score_manager._transcript.contents

    path = score_manager._configuration.example_score_packages_directory
    materials_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score', 
        'materials',
        )
    assert materials_directory in contents
    assert 'Rewriting' in contents
    assert '__metadata__.py files rewritten.' in contents