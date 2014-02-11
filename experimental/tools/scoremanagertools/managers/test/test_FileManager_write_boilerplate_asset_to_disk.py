# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_FileManager_write_boilerplate_asset_to_disk_01():

    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_manager = scoremanagertools.managers.FileManager(filesystem_path=filesystem_path)
    assert not os.path.exists(filesystem_path)

    try:
        boilerplate_file_built_in_asset_name = 'canned_testnumbers_material_definition.py'
        file_manager._write_boilerplate(boilerplate_file_built_in_asset_name)
        source = open(os.path.join(
            file_manager.boilerplate_directory_path, boilerplate_file_built_in_asset_name), 'r')
        target = open(file_manager.filesystem_path)
        assert source.readlines() == target.readlines()
        file_manager._remove()
    finally:
        if os.path.exists(filesystem_path):
            os.remove(filesystem_path)
        assert not os.path.exists(filesystem_path)
