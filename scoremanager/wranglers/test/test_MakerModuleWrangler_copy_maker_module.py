# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_MakerModuleWrangler_copy_maker_module_01():

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'makers',
        'RedExampleScoreTemplate.py',
        )
    target_path = os.path.join(
        score_manager._configuration.user_library_makers_directory_path,
        'ReusableScoreTemplate.py',
        )

    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)
    try:
        input_ = 'k cp RedExampleScoreTemplate.py'
        input_ += ' My~maker~module~library ReusableScoreTemplate y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'ReusableScoreTemplate.py' in contents
        os.remove(target_path)
    finally:
        if os.path.exists(target_path):
            os.remove(target_path)
    assert os.path.exists(source_path)
    assert not os.path.exists(target_path)