# -*- encoding: utf-8 -*-
import filecmp
import os
from abjad import *
import scoremanager
score_manager = scoremanager.core.AbjadIDE(is_test=True)


def test_MaterialPackageManager_set_autoeditor_01():

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_tempo_inventory',
        )

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score m new test~tempo~inventory y'
        input_ += ' aes TempoInventory <return> q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        string = 'test tempo inventory (AE)'
        assert string in contents


def test_MaterialPackageManager_set_autoeditor_02():
    r'''Preserves existing output.py file when appropriate.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'output.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score m tempo~inventory'
        input_ += ' aeu aes TempoInventory <return> q'
        score_manager._run(input_=input_)
        assert filecmp.cmp(path, path + '.backup')


def test_MaterialPackageManager_set_autoeditor_03():
    r'''Warns before clobbering existing output.py file.
    '''

    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'tempo_inventory',
        'output.py',
        )

    with systemtools.FilesystemState(keep=[path]):
        input_ = 'red~example~score m tempo~inventory'
        input_ += ' aeu aes ClefInventory n q'
        score_manager._run(input_=input_)
        contents = score_manager._transcript.contents
        line = 'Existing output.py file contains TempoInventory.'
        assert line in contents
        line = 'Overwrite existing output.py file?'
        assert line in contents