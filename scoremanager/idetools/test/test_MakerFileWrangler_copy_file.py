# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MakerFileWrangler_copy_file_01():

    source_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'makers',
        'RedExampleScoreTemplate.py',
        )
    target_path = os.path.join(
        ide._configuration.makers_library,
        'ReusableScoreTemplate.py',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'K cp RedExampleScoreTemplate.py'
        input_ += ' My~makers~depot ReusableScoreTemplate y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'ReusableScoreTemplate.py' in contents