# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_PackageManager_read_only_attributes_01():
    r'''Stub package.
    '''

    package_manager = scoremanagertools.managers.PackageManager(
        'scoremanagertools.materialpackages.red_sargasso_measures')
    assert package_manager.filesystem_path == os.path.join(
        package_manager.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures')
    assert package_manager._get_metadata('foo') is None
    assert package_manager.initializer_file_name == \
        os.path.join(
            package_manager.configuration.built_in_material_packages_directory_path,
            'red_sargasso_measures','__init__.py')
    assert package_manager.package_path == \
        'scoremanagertools.materialpackages.red_sargasso_measures'
    assert package_manager._space_delimited_lowercase_name == 'red sargasso measures'
