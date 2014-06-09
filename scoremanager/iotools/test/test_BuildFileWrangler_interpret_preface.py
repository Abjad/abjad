# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_interpret_preface_01():
    r'''Works when preface already exists.
    '''

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'preface.tex',
        )
    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'preface.pdf',
        )

    with systemtools.FilesystemState(keep=[source_path, path]):
        assert filecmp.cmp(path, path + '.backup')
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u pi q'
        score_manager._run(input_=input_)
        assert os.path.isfile(path)
        #assert diff-pdf(path, backup_path)