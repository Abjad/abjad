# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_set_view_01():
    r'''Works in materials depot.
    
    Makes sure only select material packages are visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.wrangler_views_directory,
        '__MaterialPackageWrangler_views__.py',
        )
    with systemtools.FilesystemState(keep=[views_file]):
        os.remove(views_file)
        input_ = 'mm wa add _test'
        input_ += ' add performer~inventory~(Red~Example~Score)'
        input_ += ' add tempo~inventory~(Red~Example~Score) done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Abjad IDE - materials depot [_test]',
            '',
            '    Red Example Score:',
            '       1: performer inventory',
            '       2: tempo inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_02():
    r'''Works in materials directory.
    
    Makes sure only select material package is visible.
    '''
    
    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(views_file)
        os.remove(metadata_file)
        input_ = 'red~example~score m wa add _test'
        input_ += ' add performer~inventory done done'
        input_ += ' ws _test q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials directory [_test]',
            '',
            '   1: performer inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_03():
    r'''Works with metadata.
    '''

    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score m ws inventories q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials directory [inventories]',
            '',
            '   1: performer inventory',
            '   2: pitch range inventory',
            '   3: tempo inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_04():
    r'''Works with :ds: display string token.

    The 'inventories' view is defined equal to "'inventory' in :ds:".
    '''

    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score m ws inventories q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials directory [inventories]',
            '',
            '   1: performer inventory',
            '   2: pitch range inventory',
            '   3: tempo inventory',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)


def test_MaterialPackageWrangler_set_view_05():
    r'''Works with :path: display string token.

    The 'magic' view is defined equal to "'magic_' in :path:".
    '''

    views_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__views__.py',
        )
    metadata_file = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        '__metadata__.py',
        )
    with systemtools.FilesystemState(keep=[views_file, metadata_file]):
        os.remove(metadata_file)
        input_ = 'red~example~score m ws magic q'
        ide._run(input_=input_)
        transcript = ide._transcript

        lines = [
            'Red Example Score (2013) - materials directory [magic]',
            '',
            '   1: magic numbers',
            '',
            '      materials - copy (cp)',
            '      materials - new (new)',
            '      materials - remove (rm)',
            '      materials - rename (ren)',
            '',
            ]
        assert any(_.lines == lines for _ in transcript)