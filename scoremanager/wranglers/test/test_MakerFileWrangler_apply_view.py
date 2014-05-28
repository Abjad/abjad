# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
score_manager = scoremanager.core.ScoreManager(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__MakerFileWrangler_views__.py',
    )


def test_MakerFileWrangler_apply_view_01():
    r'''Works in library.
    
    Makes sure only select maker file is visible.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'k vnew _test rm all'
        input_ += ' add RedExampleScoreTemplate.py~(Red~Example~Score)'
        input_ += ' done <return>'
        input_ += ' vap _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Score Manager - maker files (_test)',
            '',
            '   1: RedExampleScoreTemplate.py (Red Example Score)',
            '',
            '      maker files - copy (cp)',
            '      maker files - new (new)',
            '      maker files - remove (rm)',
            '      maker files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MakerFileWrangler_apply_view_02():
    r'''Works in score package makers directory.
    
    Makes sure only select maker file is visible.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'red~example~score k vnew _test rm all'
        input_ += ' add RedExampleScoreTemplate.py done <return>'
        input_ += ' vap _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Red Example Score (2013) - maker files (_test)',
            '',
            '   1: RedExampleScoreTemplate.py',
            '',
            '      maker files - copy (cp)',
            '      maker files - new (new)',
            '      maker files - remove (rm)',
            '      maker files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)