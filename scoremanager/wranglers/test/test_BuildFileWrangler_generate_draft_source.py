# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.core.ScoreManager(is_test=True)


def test_BuildFileWrangler_generate_draft_source_01():
    r'''Overwrites existing draft source.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory_path,
        'red_example_score',
        'build',
        'draft.tex',
        )
    backup_path = path + '.backup'

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)
    shutil.copyfile(path, backup_path)
    assert os.path.exists(backup_path)

    try:
        input_ = 'red~example~score u dg y y q'
        score_manager._run(pending_user_input=input_)
        contents = score_manager._transcript.contents
        assert '- build files' in contents
        assert 'Overwrite' in contents
        assert 'Will assemble segments in this order:' in contents
        assert 'Overwrote' in contents
        assert os.path.isfile(path)
        assert filecmp.cmp(path, backup_path)
    finally:
        shutil.move(backup_path, path)

    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)