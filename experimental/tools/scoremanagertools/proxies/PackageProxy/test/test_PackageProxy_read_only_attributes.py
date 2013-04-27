import os
from experimental import *


def test_PackageProxy_read_only_attributes_01():
    '''Stub package.
    '''

    package_proxy = scoremanagertools.proxies.PackageProxy('materials.red_sargasso_measures')
    assert package_proxy.path == \
        os.path.join(package_proxy.configuration.SCORE_MANAGER_MATERIALS_DIRECTORY_PATH, 'red_sargasso_measures')
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.initializer_file_name == \
        os.path.join(
            package_proxy.configuration.SCORE_MANAGER_MATERIALS_DIRECTORY_PATH, 
            'red_sargasso_measures','__init__.py')
    assert package_proxy.package_path == 'materials.red_sargasso_measures'
    assert package_proxy.name == 'red_sargasso_measures'
    assert package_proxy.human_readable_name == 'red sargasso measures'
    assert package_proxy.parent_initializer_file_name == \
        os.path.join(package_proxy.configuration.SCORE_MANAGER_MATERIALS_DIRECTORY_PATH, '__init__.py')
    assert package_proxy.parent_package_path == 'materials'
