# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_generate_front_cover_source_01():
    r'''Works when front cover source already exists.

    (Front cover source already exists in Red Example Score.)
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score u fcg y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert 'Overwrite' in contents
        assert 'Overwrote' in contents
        assert filecmp.cmp(path, path + '.backup')


def test_BuildFileWrangler_generate_front_cover_source_02():
    r'''Works when front cover source doesn't exist.

    (Front cover source does exist in Red Example Score.)
    '''

    path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'front-cover.tex',
        )

    with systemtools.FilesystemState(keep=[path]):
        os.remove(path)
        assert not os.path.exists(path)
        input_ = 'red~example~score u fcg q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert 'Overwrite' not in contents
        assert 'Overwrote' not in contents
        assert filecmp.cmp(path, path + '.backup')