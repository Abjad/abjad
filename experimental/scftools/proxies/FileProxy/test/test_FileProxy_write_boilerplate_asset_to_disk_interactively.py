import os
import scftools


def test_FileProxy_write_boilerplate_asset_to_disk_interactively_01():

    path_name = os.path.join(os.environ.get('SCFPATH'), 'temporary_file.txt')
    file_proxy = scftools.proxies.FileProxy(path_name=path_name)
    assert not os.path.exists(path_name)

    try:
        boilerplate_asset_name = 'canned_testnumbers_material_definition.py'
        user_input = '{} q'.format(boilerplate_asset_name)
        file_proxy.write_boilerplate_asset_to_disk_interactively(user_input=user_input)
        source = open(os.path.join(file_proxy.boilerplate_directory_name, boilerplate_asset_name), 'r')
        target = open(file_proxy.path_name)
        assert source.readlines() == target.readlines()
        file_proxy.remove()
    finally:
        if os.path.exists(path_name):
            os.remove(path_name)
        assert not os.path.exists(path_name)
