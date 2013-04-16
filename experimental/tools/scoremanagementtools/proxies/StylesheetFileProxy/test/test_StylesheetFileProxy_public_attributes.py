import os
from experimental import *


def test_StylesheetFileProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scoremanagementtools.proxies.StylesheetFileProxy()

    assert proxy.breadcrumb == 'stylesheet file proxy'
    assert not proxy.exists
    assert not proxy.file_lines
    assert proxy.generic_class_name == 'stylesheet'
    assert proxy.human_readable_name is None
    assert not proxy.is_versioned
    assert proxy.parent_directory_name is None
    assert proxy.path_name is None
    assert proxy.plural_generic_class_name == 'stylesheets'
    assert proxy.short_name is None
    assert proxy.short_name_without_extension is None
    assert proxy.svn_add_command is None
    assert proxy.temporary_asset_short_name == 'temporary_stylesheet.ly'


def test_StylesheetFileProxy_public_attributes_02():
    '''With path.
    '''

    short_name = 'clean_letter_14.ly'
    path_name = os.path.join(os.environ.get('SCFPATH'), 'stylesheets', short_name)
    proxy = scoremanagementtools.proxies.StylesheetFileProxy(path_name)

    assert proxy.breadcrumb == 'clean_letter_14.ly'
    assert proxy.exists
    assert proxy.file_lines
    assert proxy.generic_class_name == 'stylesheet'
    assert proxy.human_readable_name == short_name
    assert proxy.is_versioned
    assert proxy.parent_directory_name == proxy.stylesheets_directory_name
    assert proxy.path_name == path_name
    assert proxy.plural_generic_class_name == 'stylesheets'
    assert proxy.short_name == short_name
    assert proxy.short_name_without_extension == short_name[:-3]
    assert proxy.svn_add_command == 'svn add {}'.format(proxy.path_name)
    assert proxy.temporary_asset_short_name == 'temporary_stylesheet.ly'
