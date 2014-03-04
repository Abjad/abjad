# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_FileManager__write_boilerplate_01():

    configuration = scoremanager.core.ScoreManagerConfiguration()
    path = os.path.join(
        configuration.score_manager_directory_path, 
        'temporary_file.txt',
        )
    file_manager = scoremanager.managers.FileManager(
        path=path,
        )
    assert not os.path.exists(path)

    try:
        string = 'boilerplate_testnumbers_material_definition.py'
        boilerplate_file_abjad_asset_name = string
        file_manager._write_boilerplate(boilerplate_file_abjad_asset_name)
        file_path = os.path.join(
            file_manager._configuration.boilerplate_directory_path, 
            boilerplate_file_abjad_asset_name
            )
        source = open(file_path, 'r')
        target = open(file_manager._path)
        assert source.readlines() == target.readlines()
        file_manager._remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)
