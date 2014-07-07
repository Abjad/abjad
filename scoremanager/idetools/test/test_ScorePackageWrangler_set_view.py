# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_ScorePackageWrangler_set_view_01():
    r'''Makes sure only select scores are visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__ScorePackageWrangler_views__.py',
        )
    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = 'wa add _test'
        input_ += ' add Red~Example~Score~(2013) done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript
        lines = [
            'Abjad IDE - scores [_test]',
            '',
            '   1: Red Example Score (2013)',
            '',
            '      scores - copy (cp)',
            '      scores - new (new)',
            '      scores - remove (rm)',
            '      scores - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)