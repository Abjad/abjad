# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager

# must be is_test=False to test views
score_manager = scoremanager.core.ScoreManager(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__BuildFileWrangler_views__.py',
    )


def test_BuildFileWrangler_clear_view_01():
    r'''In library: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'u vnew _test rm all'
    input_ += ' add segment-01.ly~(Red~Example~Score) done <return>'
    input_ += ' vap _test vcl vrm _test <return> q'

    with systemtools.FilesystemState(keep=[views_file]):
        score_manager._run(input_=input_)
    transcript = score_manager._transcript

    lines = [
        'Score Manager - build files (_test)',
        '',
        '   1: segment-01.ly (Red Example Score)',
        '',
        '      files - copy (cp)',
        '      files - new (new)',
        '      files - remove (rm)',
        '      files - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)


def test_BuildFileWrangler_clear_view_02():
    r'''In single build directory: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    input_ = 'red~example~score u vnew _test rm all'
    input_ += ' add segment-01.ly done <return>'
    input_ += ' vap _test vcl vrm _test <return> q'

    with systemtools.FilesystemState(keep=[views_file]):
        score_manager._run(input_=input_)
    transcript = score_manager._transcript

    lines = [
        'Red Example Score (2013) - build files (_test)',
        '',
        '   1: segment-01.ly',
        '',
        '      files - copy (cp)',
        '      files - new (new)',
        '      files - remove (rm)',
        '      files - rename (ren)',
        '',
        ]
    assert any(_.lines == lines for _ in transcript)