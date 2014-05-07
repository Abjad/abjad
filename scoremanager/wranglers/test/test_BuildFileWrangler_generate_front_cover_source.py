# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_generate_front_cover_source_01():
    r'''Works when front cover source already exists.

    (Front cover source already exists in Red Example Score.)
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    try:
        shutil.copyfile(path, backup_path)
        assert os.path.isfile(backup_path)
        input_ = 'red~example~score u fcg y q'
        score_manager._run(pending_input=input_)
        contents = score_manager._transcript.contents
        assert 'Overwrite' in contents
        assert 'Overwrote' in contents
        assert filecmp.cmp(path, backup_path)
    finally:
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, path)
        if os.path.exists(backup_path):
            os.remove(backup_path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)


def test_BuildFileWrangler_generate_front_cover_source_02():
    r'''Works when front cover source doesn't exist.

    (Front cover source does exist in Red Example Score.)
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    try:
        shutil.copyfile(path, backup_path)
        assert os.path.isfile(backup_path)
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u fcg q'
        score_manager._run(pending_input=input_)
        contents = score_manager._transcript.contents
        assert 'Overwrite' not in contents
        assert 'Overwrote' not in contents
        assert filecmp.cmp(path, backup_path)
    finally:
        if os.path.exists(backup_path):
            shutil.copyfile(backup_path, path)
        if os.path.exists(backup_path):
            os.remove(backup_path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)