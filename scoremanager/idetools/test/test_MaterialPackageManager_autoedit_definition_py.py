# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_MaterialPackageManager_autoedit_definition_py_01():
    r'''Target tempo inventory.
    '''

    score_manager = scoremanager.idetools.AbjadIDE(is_test=True)
    configuration = score_manager._configuration
    path = os.path.join(
        score_manager._configuration.example_score_packages_directory,
        'red_example_score',
        'materials',
        'test_tempo_inventory',
        )
    directory_entries = [
        '__init__.py',
        '__metadata__.py',
        'definition.py',
        'versions',
        ]
    inventory = indicatortools.TempoInventory([
        ((1, 4), 60),
        ((1, 4), 90),
        ])

    assert not os.path.exists(path)

    with systemtools.FilesystemState(remove=[path]):
        input_ = 'red~example~score m new test~tempo~inventory y'
        input_ += ' dae y TempoInventory'
        input_ += ' add ((1, 4), 60) add ((1, 4), 90) done'
        input_ += ' done y q'
        score_manager._run(input_=input_)
        assert os.path.exists(path)
        session = scoremanager.idetools.Session(is_test=True)
        manager = scoremanager.idetools.MaterialPackageManager
        manager = manager(path=path, session=session)
        assert manager._list() == directory_entries
        target = manager._execute_definition_py()
        assert target == inventory