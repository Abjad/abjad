# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_copy_package_01():
    r'''Works in materials depot.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packges only (because copying into example score packages could pollute the
    example score packages).
    '''

    input_ = 'mm cp performer~inventory~(Red~Example~Score) q'
    ide._run(input_=input_)
    contents = ide._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials depot',
        'Abjad IDE - materials depot',
        ]
    assert ide._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_MaterialPackageWrangler_copy_package_02():
    r'''Works in materials directory.
    '''

    source_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'performer_inventory',
        )
    target_path = os.path.join(
        ide._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'copied_performer_inventory',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score m cp'
        input_ += ' performer~inventory copied~performer~inventory y q'
        ide._run(input_=input_)
        contents = ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_performer_inventory' in contents


def test_MaterialPackageWrangler_copy_package_03():
    r'''Includes preservation message in getter help.
    '''

    input_ = 'red~example~score m cp tempo~inventory ? q'
    ide._run(input_=input_)
    contents = ide._transcript.contents
        
    string = 'Existing material package name> tempo_inventory'
    assert string in contents
    string = 'Value must be string. Press <return> to preserve existing name.'
    assert string in contents