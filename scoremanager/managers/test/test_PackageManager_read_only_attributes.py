# -*- encoding: utf-8 -*-
import os
from abjad import *
import scoremanager
configuration = scoremanager.core.ScoreManagerConfiguration()


def test_PackageManager_read_only_attributes_01():
    r'''Stub package.
    '''

    string = 'scoremanager.materials.example_sargasso_measures'
    file_path = os.path.join(
        configuration.abjad_material_packages_directory_path, 
        'example_sargasso_measures',
        )
    package_manager = scoremanager.managers.PackageManager(file_path)
    assert package_manager._filesystem_path == file_path
    assert package_manager._get_metadatum('foo') is None
    file_path = os.path.join(
        package_manager._configuration.abjad_material_packages_directory_path,
        'example_sargasso_measures','__init__.py',
        )
    assert package_manager._initializer_file_path == file_path
    string = 'scoremanager.materials.example_sargasso_measures'
    assert package_manager._package_path == string
    string = 'example sargasso measures'
    assert package_manager._space_delimited_lowercase_name == string
