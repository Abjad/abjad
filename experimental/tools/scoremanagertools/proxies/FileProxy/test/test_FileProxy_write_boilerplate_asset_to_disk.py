import os
from experimental import *


def test_FileProxy_write_boilerplate_asset_to_disk_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(file_path=file_path)
    assert not os.path.exists(file_path)

    try:
        boilerplate_asset_name = 'canned_testnumbers_material_definition.py'
        file_proxy.write_boilerplate_asset_to_disk(boilerplate_asset_name)
        source = open(os.path.join(
            file_proxy.configuration.boilerplate_directory_path, boilerplate_asset_name), 'r')
        target = open(file_proxy.path)
        assert source.readlines() == target.readlines()
        file_proxy.remove()
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        assert not os.path.exists(file_path)
