# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False to test views
score_manager = scoremanager.ide.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__DistributionFileWrangler_views__.py',
    )


def test_DistributionFileWrangler_clear_view_01():
    r'''In library: applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'd vnew _test rm all'
        input_ += ' add red-example-score.pdf~(Red~Example~Score) done'
        input_ += ' <return> vap _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Abjad IDE - distribution files [_test]',
            '',
            '   1: red-example-score.pdf (Red Example Score)',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_DistributionFileWrangler_clear_view_02():
    r'''In score package distribution directory: 
    applies view and then clears view.

    Makes sure only one file is visible when view is applied.
    
    Then makes sure multiple files are visible once view is cleared.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'red~example~score d vnew _test rm all'
        input_ += ' add red-example-score.pdf done <return>'
        input_ += ' vap _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Red Example Score (2013) - distribution files [_test]',
            '',
            '   1: red-example-score.pdf',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)