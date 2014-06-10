# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_generate_draft_source_01():
    r'''Overwrites existing draft source.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'draft.tex',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score u dg y y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert 'Overwrite' in contents
        assert 'Will assemble segments in this order:' in contents
        assert 'Overwrote' in contents
        assert os.path.isfile(path)
        assert filecmp.cmp(path, path + '.backup')


def test_BuildFileWrangler_generate_draft_source_02():
    r'''Works with empty build directory.

    (Blue Example Score segment __views.py__ is intentionally corrupt.)
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'blue_example_score',
        'build',
        'draft.tex',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'blue~example~score u dg y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        message = 'SegmentPackageWrangler views.py is corrupt.' 
        assert message not in contents
        assert 'Will assemble segments in this order:' in contents
        assert os.path.isfile(path)


def test_BuildFileWrangler_generate_draft_source_03():
    r'''Works when no segments have been created.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'etude_example_score',
        'build',
        'draft.tex',
        )

    with systemtools.FilesystemState(keep=[path]):

        input_ = 'etude~example~score u dg y y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert 'Overwrite' in contents
        assert 'No segments found:' in contents
        assert 'will generate source without segments' in contents
        assert 'Overwrote' in contents
        assert os.path.isfile(path)
        assert filecmp.cmp(path, path + '.backup')