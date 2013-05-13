import os
from experimental import *


def test_StylesheetFileProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scoremanagertools.proxies.StylesheetFileProxy()

    assert proxy._breadcrumb == 'stylesheet file proxy'
    assert not proxy.exists()
    assert not proxy.file_lines
    assert proxy._generic_class_name == 'stylesheet'
    assert proxy._space_delimited_lowercase_name is None
    assert not proxy.is_versioned()
    assert proxy.filesystem_directory_name is None
    assert proxy.filesystem_path is None
    assert proxy._plural_generic_class_name == 'stylesheets'
    assert proxy.filesystem_basename is None
    assert proxy._svn_add_command is None
    assert proxy._temporary_asset_name == 'temporary_stylesheet.ly'


def test_StylesheetFileProxy_public_attributes_02():
    '''With path.
    '''

    file_name = 'clean_letter_14.ly'
    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'built_in_stylesheets', file_name)
    proxy = scoremanagertools.proxies.StylesheetFileProxy(filesystem_path)

    assert proxy._breadcrumb == 'clean_letter_14.ly'
    assert proxy.exists()
    assert proxy.file_lines
    assert proxy._generic_class_name == 'stylesheet'
    assert proxy._space_delimited_lowercase_name == file_name
    assert proxy.is_versioned()
    assert proxy.filesystem_path == filesystem_path
    assert proxy._plural_generic_class_name == 'stylesheets'
    assert proxy.filesystem_basename == file_name
    assert proxy._svn_add_command == 'svn add {}'.format(proxy.filesystem_path)
    assert proxy._temporary_asset_name == 'temporary_stylesheet.ly'
