# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_ScorePackageManager_check_package_01():

    input_ = 'red~example~score ck y q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        'Build files (18 files): OK',
        'Distribution files (2 files): OK',
        'Maker files (2 files): OK',
        'Materials (5 packages):',
        'Segments (3 packages):',
        'Stylesheets (2 files): OK',
        ]
    for line in lines:
        assert line in contents
    assert 'found' not in contents


def test_ScorePackageManager_check_package_02():

    input_ = 'red~example~score ck n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    lines = [
        '6 of 6 required directories found:',
        '2 of 2 required files found:',
        '1 optional directory found:',
        ]
    for line in lines:
        assert line in contents


def test_ScorePackageManager_check_package_03():

    extra_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'extra_file.txt',
        )

    with systemtools.FilesystemState(remove=[extra_file]):
        with open(extra_file, 'w') as file_pointer:
            file_pointer.write('')
        input_ = 'red~example~score ck y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents

    line = '1 unrecognized file found:'
    assert line in contents