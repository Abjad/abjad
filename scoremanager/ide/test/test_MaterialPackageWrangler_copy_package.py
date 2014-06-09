# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.ide.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_copy_package_01():
    r'''Works in library.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packges only (because copying into example score packages could pollute the
    example score packages).
    '''

    input_ = 'm cp instrumentation~(Red~Example~Score) q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - materials',
        'Abjad IDE - materials',
        ]
    assert score_manager._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_MaterialPackageWrangler_copy_package_02():
    r'''Works in score.
    '''

    source_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'instrumentation',
        )
    target_path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'copied_instrumentation',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score m cp'
        input_ += ' instrumentation copied_instrumentation y q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied_instrumentation' in contents


def test_MaterialPackageWrangler_copy_package_03():
    r'''Includes preservation message in getter help.
    '''

    input_ = 'red~example~score m cp tempo~inventory ? q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
        
    string = 'Existing material package name> tempo_inventory'
    assert string in contents
    string = 'Value must be string. Press <return> to preserve existing name.'
    assert string in contents