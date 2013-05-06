import os
from experimental import *


def test_StylesheetFileProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scoremanagertools.proxies.StylesheetFileProxy()

    assert proxy.breadcrumb == 'stylesheet file proxy'
    assert not proxy.exists
    assert not proxy.file_lines
    assert proxy._generic_class_name == 'stylesheet'
    assert proxy.space_delimited_lowercase_name is None
    assert not proxy.is_versioned
    assert proxy.parent_directory_path is None
    assert proxy.file_path is None
    assert proxy._plural_generic_class_name == 'stylesheets'
    assert proxy.filesystem_basename is None
    assert proxy.name_without_extension is None
    assert proxy._svn_add_command is None
    assert proxy._temporary_asset_name == 'temporary_stylesheet.ly'


def test_StylesheetFileProxy_public_attributes_02():
    '''With path.
    '''

    file_name = 'clean_letter_14.ly'
    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', file_name)
    proxy = scoremanagertools.proxies.StylesheetFileProxy(file_path)

    assert proxy.breadcrumb == 'clean_letter_14.ly'
    assert proxy.exists
    assert proxy.file_lines
    assert proxy._generic_class_name == 'stylesheet'
    assert proxy.space_delimited_lowercase_name == file_name
    assert proxy.is_versioned
    assert proxy.parent_directory_path == proxy.configuration.stylesheets_directory_path
    assert proxy.file_path == file_path
    assert proxy._plural_generic_class_name == 'stylesheets'
    assert proxy.filesystem_basename == file_name
    assert proxy.name_without_extension == file_name[:-3]
    assert proxy._svn_add_command == 'svn add {}'.format(proxy.file_path)
    assert proxy._temporary_asset_name == 'temporary_stylesheet.ly'
