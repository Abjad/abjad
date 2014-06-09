# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
score_manager = scoremanager.iotools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_check_every_package_01():
    r'''Works in score.
    '''

    lines = [
        'Materials (5 packages)',
        'Magic numbers: OK',
        'Time signatures: OK',
        'Instrumentation: OK',
        'Pitch range inventory: OK',
        'Tempo inventory: OK',
        ]

    input_ = 'red~example~score m ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents


def test_MaterialPackageWrangler_check_every_package_02():
    r'''Works in library.
    '''

    lines = [
        'Magic numbers (Red Example Score): OK',
        'Time signatures (Red Example Score): OK',
        'Instrumentation (Red Example Score): OK',
        'Pitch range inventory (Red Example Score): OK',
        'Tempo inventory (Red Example Score): OK',
        ]

    input_ = 'm ck* y n q'
    score_manager._run(input_=input_)
    contents = score_manager._transcript.contents
    for line in lines:
        assert line in contents

def test_MaterialPackageWrangler_check_every_package_03():
    r'''Supplies missing directory and missing file.
    '''

    material_directory = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        )
    versions_directory = os.path.join(material_directory, 'versions')
    initializer = os.path.join(material_directory, '__init__.py')
        
    with systemtools.FilesystemState(keep=[versions_directory, initializer]):
        os.remove(initializer)
        shutil.rmtree(versions_directory)
        input_ = 'red~example~score m ck* y y q'
        score_manager._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)