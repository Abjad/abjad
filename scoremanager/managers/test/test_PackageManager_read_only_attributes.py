# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager


def test_PackageManager_read_only_attributes_01():
    r'''Stub package.
    '''

    string = 'scoremanager.materialpackages.red_sargasso_measures'
    package_manager = scoremanager.managers.PackageManager(string)
    file_path = os.path.join(
        package_manager.configuration.built_in_material_packages_directory_path, 
        'red_sargasso_measures',
        )
    assert package_manager.filesystem_path == file_path
    assert package_manager._get_metadatum('foo') is None
    file_path = os.path.join(
        package_manager.configuration.built_in_material_packages_directory_path,
        'red_sargasso_measures','__init__.py',
        )
    assert package_manager.initializer_file_path == file_path
    string = 'scoremanager.materialpackages.red_sargasso_measures'
    assert package_manager.package_path == string
    string = 'red sargasso measures'
    assert package_manager._space_delimited_lowercase_name == string
