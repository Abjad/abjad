import os
from experimental import *


def test_FileProxy_write_boilerplate_asset_to_disk_01():

    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH, 'temporary_file.txt')
    file_proxy = scoremanagertools.proxies.FileProxy(path_name=path)
    assert not os.path.exists(path)

    try:
        boilerplate_asset_name = 'canned_testnumbers_material_definition.py'
        file_proxy.write_boilerplate_asset_to_disk(boilerplate_asset_name)
        source = open(os.path.join(
            file_proxy.configuration.boilerplate_directory_name, boilerplate_asset_name), 'r')
        target = open(file_proxy.path_name)
        assert source.readlines() == target.readlines()
        file_proxy.remove()
    finally:
        if os.path.exists(path):
            os.remove(path)
        assert not os.path.exists(path)
