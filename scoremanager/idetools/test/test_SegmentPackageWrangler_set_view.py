# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
# must have is_test=False to test view application
score_manager = scoremanager.idetools.AbjadIDE(is_test=False)


def test_SegmentPackageWrangler_set_view_01():
    r'''In library. Applies view.
    
    Makes sure only one segment is visible after view is applied.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__SegmentPackageWrangler_views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.wrangler_views_directory,
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        input_ = 'G vnew _test rm 1-99'
        input_ += ' add A~(Red~Example~Score) done'
        input_ += ' vs _test vrm _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Abjad IDE - segments [_test]',
            '',
            '    Red Example Score:',
            '       1: A',
            '',
            '      segments - copy (cp)',
            '      segments - new (new)',
            '      segments - remove (rm)',
            '      segments - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_SegmentPackageWrangler_set_view_02():
    r'''In score package. Applies view.
    
    Makes sure only one segment is visible after view is applied.
    '''
    
    views_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        '__views__.py',
        )
    metadata_file = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        input_ = 'red~example~score g vnew _test'
        input_ += ' rm all add A done'
        input_ += ' vs _test vrm _test q'
        score_manager._run(input_=input_)
        transcript = score_manager._transcript
        lines = [
            'Red Example Score (2013) - segments [_test]',
            '',
            '   1: A',
            '',
            '      segments - copy (cp)',
            '      segments - new (new)',
            '      segments - remove (rm)',
            '      segments - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)