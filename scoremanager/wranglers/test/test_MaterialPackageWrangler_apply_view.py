# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must be is_test=False for view tests
score_manager = scoremanager.core.AbjadIDE(is_test=False)
views_file = os.path.join(
    score_manager._configuration.wrangler_views_directory,
    '__MaterialPackageWrangler_views__.py',
    )


def test_MaterialPackageWrangler_apply_view_01():
    r'''Works in library.
    
    Makes sure only select material packages are visible.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'm vnew _test rm all'
        input_ += ' add instrumentation~(Red~Example~Score)'
        input_ += ' add tempo~inventory~(Red~Example~Score) done <return>'
        input_ += ' vap _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Abjad IDE - materials (_test)',
            '',
            '   1: instrumentation (Red Example Score)',
            '   2: tempo inventory (Red Example Score)',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)


def test_MaterialPackageWrangler_apply_view_02():
    r'''Works in score.
    
    Makes sure only select material package is visible.
    '''
    
    with systemtools.FilesystemState(keep=[views_file]):
        input_ = 'red~example~score m vnew _test rm all'
        input_ += ' add instrumentation done <return>'
        input_ += ' vap _test vrm _test <return> q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript

        lines = [
            'Red Example Score (2013) - materials (_test)',
            '',
            '   1: instrumentation (AE)',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)