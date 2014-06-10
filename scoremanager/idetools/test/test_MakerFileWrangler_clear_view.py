# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False to test views
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__MakerFileWrangler_views__.py',
    )


def test_MakerFileWrangler_clear_view_01():
    r'''In library: applies view and then clears view.

    Makes sure only one maker file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'k vnew _test rm all'
        input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
        input_ += ' done <return>'
        input_ += ' vap _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Abjad IDE - maker files [_test]',
            '',
            '   1: RedExampleScoreTemplate.py (Red Example Score)',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MakerFileWrangler_clear_view_02():
    r'''In single makers directory: applies view and then clears view.

    Makes sure only one maker file is visible when view is applied.
    
    Then makes sure multiple maker files are visible once view is cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'red~example~score k vnew _test rm all'
        input_ += ' add RedExampleScoreTemplate.py done <return>'
        input_ += ' vap _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Red Example Score (2013) - maker files [_test]',
            '',
            '   1: RedExampleScoreTemplate.py',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)