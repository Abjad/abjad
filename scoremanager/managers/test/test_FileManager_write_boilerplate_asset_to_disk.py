# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager_write_boilerplate_asset_to_disk_01():

    configuration = scoremanager.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        filesystem_path=filesystem_path,
        )
    assert not os.path.exists(filesystem_path)

    try:
        string = 'boilerplate_testnumbers_material_definition.py'
        boilerplate_file_built_in_asset_name = string
        file_manager._write_boilerplate(boilerplate_file_built_in_asset_name)
        file_path = os.path.join(
            file_manager.boilerplate_directory_path, 
            boilerplate_file_built_in_asset_name
            )
        source = open(file_path, 'r')
        target = open(file_manager.filesystem_path)
        assert source.readlines() == target.readlines()
        file_manager._remove()
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
