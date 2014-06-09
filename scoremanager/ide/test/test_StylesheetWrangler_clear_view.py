# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False to test view application
score_manager = scoremanager.ide.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__StylesheetWrangler_views__.py',
    )


def test_StylesheetWrangler_clear_view_01():
    r'''Makes sure more than one stylesheet is visible without view.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'y vnew _test rm all add clean-letter-14.ily~(Abjad)'
        input_ += ' done <return> vap _test vcl vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - stylesheets [_test]',
            '',
            '   1: clean-letter-14.ily (Abjad)',
            '',
            '      files - copy (cp)',
            '      files - new (new)',
            '      files - remove (rm)',
            '      files - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)