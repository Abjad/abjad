# -*- encoding: utf-8 -*-
import filecmp
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_generate_draft_source_01():
    r'''Preserves existing draft when candidate compares equal.
    '''

    draft_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'draft.tex',
        )

    with systemtools.FilesystemState(keep=[draft_path]):
        input_ = 'red~example~score u dg y y q'
        ide._run(input_=input_)

    contents = ide._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents


def test_BuildFileWrangler_generate_draft_source_02():
    r'''Works with empty build directory.

    (Blue Example Score segment __views.py__ is intentionally corrupt.)
    '''

    draft_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'blue_example_score',
        'build',
        'draft.tex',
        )

    with systemtools.FilesystemState(remove=[draft_path]):
        input_ = 'blue~example~score u dg y q'
        ide._run(input_=input_)
        assert os.path.isfile(draft_path)

    contents = ide._transcript.contents
    message = 'SegmentPackageWrangler views.py is corrupt.' 
    assert message not in contents
    assert 'Will assemble segments in this order:' in contents
    assert 'Wrote' in contents


def test_BuildFileWrangler_generate_draft_source_03():
    r'''Works when no segments have been created.
    '''

    draft_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'etude_example_score',
        'build',
        'draft.tex',
        )

    with systemtools.FilesystemState(keep=[draft_path]):
        input_ = 'etude~example~score u dg y y q'
        ide._run(input_=input_)
        assert os.path.isfile(draft_path)
        assert filecmp.cmp(draft_path, draft_path + '.backup')

    contents = ide._transcript.contents
    message = 'No segments found: will generate source without segments'
    assert message in contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents