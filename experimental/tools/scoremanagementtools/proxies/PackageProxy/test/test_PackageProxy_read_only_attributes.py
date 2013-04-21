import os
from experimental import *


def test_PackageProxy_read_only_attributes_01():
    '''Stub package.
    '''

    package_proxy = scoremanagementtools.proxies.PackageProxy('materials.red_sargasso_measures')
    assert package_proxy.path_name == \
        os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_MATERIALS_PATH'), 'red_sargasso_measures')
    assert package_proxy.get_tag('foo') is None
    assert package_proxy.initializer_file_name == \
        os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_MATERIALS_PATH'), 'red_sargasso_measures','__init__.py')
    assert package_proxy.importable_name == 'materials.red_sargasso_measures'
    assert package_proxy.short_name == 'red_sargasso_measures'
    assert package_proxy.human_readable_name == 'red sargasso measures'
    assert package_proxy.parent_initializer_file_name == \
        os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_MATERIALS_PATH'), '__init__.py')
    assert package_proxy.parent_package_importable_name == 'materials'
