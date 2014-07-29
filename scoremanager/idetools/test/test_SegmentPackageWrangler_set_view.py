# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_SegmentPackageWrangler_set_view_01():
    r'''In segments depot. Applies view.
    
    Makes sure only one segment is visible after view is applied.
    '''
    
    views_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__SegmentPackageWrangler_views__.py',
        )
    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = 'gg wa add _test'
        input_ += ' add A~(Red~Example~Score) done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript
        lines = [
            'Abjad IDE - segments depot [_test]',
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
    r'''In segments directory. Applies view.
    
    Makes sure only one segment is visible after view is applied.
    '''
    
    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'segments',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'red~example~score g wa add _test'
        input_ += ' add A done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript
        lines = [
            'Red Example Score (2013) - segments directory [_test]',
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