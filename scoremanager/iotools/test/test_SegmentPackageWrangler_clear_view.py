# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False to test view application
score_manager = scoremanager.iotools.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__SegmentPackageWrangler_views__.py',
    )

def test_SegmentPackageWrangler_clear_view_01():
    r'''Makes sure more than one segment is visible without view.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'g vnew _test rm all'
        input_ += ' add A~(Red~Example~Score) done <return>'
        input_ += ' vap _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - segments [_test]',
            '',
            '   1: A (Red Example Score)',
            '',
            '      segments - copy (cp)',
            '      segments - new (new)',
            '      segments - remove (rm)',
            '      segments - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)