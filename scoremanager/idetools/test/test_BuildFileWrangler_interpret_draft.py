# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_interpret_draft_01():
    r'''Works when draft already exists.
    '''

    source_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'draft.tex',
        )
    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'draft.pdf',
        )

    backup_path = path + '.backup'
    assert os.path.isfile(source_path)
    assert os.path.isfile(path)
    assert not os.path.exists(backup_path)

    with systemtools.FilesystemState(keep=[source_path, path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u di q'
        ide._run(input_=input_)
        assert os.path.isfile(path)
        # TODO: make this work
        #assert systemtools.TestManager.compare_pdfs(path, path + '.backup')