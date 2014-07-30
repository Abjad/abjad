# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import scoremanager
ide = scoremanager.idetools.AbjadIDE(is_test=True)


def test_MaterialPackageWrangler_check_every_package_01():
    r'''Works in score.
    '''

    lines = [
        'Materials directory (5 packages)',
        'Magic numbers: OK',
        'Performer inventory: OK',
        'Pitch range inventory: OK',
        'Tempo inventory: OK',
        'Time signatures: OK',
        ]

    input_ = 'red~example~score m ck* y n q'
    ide._run(input_=input_)
    contents = ide._transcript.contents
    for line in lines:
        assert line in contents


def test_MaterialPackageWrangler_check_every_package_02():
    r'''Works in library.
    '''

    lines = [
        'Magic numbers (Red Example Score): OK',
        'Performer inventory (Red Example Score): OK',
        'Pitch range inventory (Red Example Score): OK',
        'Tempo inventory (Red Example Score): OK',
        'Time signatures (Red Example Score): OK',
        ]

    input_ = 'mm ck* y n q'
    ide._run(input_=input_)
    contents = ide._transcript.contents
    for line in lines:
        assert line in contents

def test_MaterialPackageWrangler_check_every_package_03():
    r'''Supplies missing directory and missing file.
    '''

    material_directory = os.path.join(
        ide._configuration.example_score_packages_directory,
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
        ide._run(input_=input_)
        assert os.path.isfile(initializer)
        assert os.path.isdir(versions_directory)