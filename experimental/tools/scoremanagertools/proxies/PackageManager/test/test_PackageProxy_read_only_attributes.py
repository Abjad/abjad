# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_PackageManager_read_only_attributes_01():
    r'''Stub package.
    '''

    package_proxy = scoremanagertools.proxies.PackageManager(
        'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures')
    assert package_proxy.filesystem_path == os.path.join(
        package_proxy.configuration.built_in_material_packages_directory_path, 'red_sargasso_measures')
    assert package_proxy._get_metadata('foo') is None
    assert package_proxy.initializer_file_name == \
        os.path.join(
            package_proxy.configuration.built_in_material_packages_directory_path,
            'red_sargasso_measures','__init__.py')
    assert package_proxy.package_path == \
        'experimental.tools.scoremanagertools.materialpackages.red_sargasso_measures'
    assert package_proxy._space_delimited_lowercase_name == 'red sargasso measures'
