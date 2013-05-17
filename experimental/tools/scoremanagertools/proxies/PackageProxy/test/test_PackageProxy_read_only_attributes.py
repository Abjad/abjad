import os
from experimental import *


def test_PackageProxy_read_only_attributes_01():
    '''Stub package.
    '''

    package_proxy = scoremanagertools.proxies.PackageProxy(
        'experimental.tools.scoremanagertools.built_in_materials.red_sargasso_measures')
    assert package_proxy.filesystem_path == os.path.join(
        package_proxy.configuration.built_in_materials_directory_path, 'red_sargasso_measures')
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.initializer_file_name == \
        os.path.join(
            package_proxy.configuration.built_in_materials_directory_path,
            'red_sargasso_measures','__init__.py')
    assert package_proxy.package_path == \
        'experimental.tools.scoremanagertools.built_in_materials.red_sargasso_measures'
    assert package_proxy.filesystem_basename == 'red_sargasso_measures'
    assert package_proxy._space_delimited_lowercase_name == 'red sargasso measures'
    assert package_proxy.parent_initializer_file_name == \
        os.path.join(package_proxy.configuration.built_in_materials_directory_path, '__init__.py')
    assert package_proxy.parent_package_path == \
        'experimental.tools.scoremanagertools.built_in_materials'
