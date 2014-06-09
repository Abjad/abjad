# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_copy_file_01():

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'RedExampleScoreTemplate.py',
        )
    target_path = os.path.join(
        score_manager._configuration.user_library_makers_directory,
        'ReusableScoreTemplate.py',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'k cp RedExampleScoreTemplate.py'
        input_ += ' My~maker~files ReusableScoreTemplate y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'ReusableScoreTemplate.py' in contents