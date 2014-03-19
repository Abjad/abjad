# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager__write_boilerplate_01():

    configuration = scoremanager.core.ScoreManagerConfiguration()
    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary-file.txt',
        )
    session = scoremanager.core.Session(is_test=True)
    manager = scoremanager.managers.FileManager(path=path, session=session)
    file_name = 'numbers_definition.py'

    assert not os.path.exists(path)
    try:
        manager._write_boilerplate(file_name)
        file_path = os.path.join(
            manager._configuration.boilerplate_directory_path, 
            file_name,
            )
        source = open(file_path, 'r')
        target = open(manager._path)
        assert source.readlines() == target.readlines()
        manager._remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
    assert not os.path.exists(path)
