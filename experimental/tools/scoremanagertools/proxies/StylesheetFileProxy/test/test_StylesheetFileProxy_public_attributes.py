import os
from experimental import *


def test_StylesheetFileProxy_public_attributes_01():
    '''Without path.
    '''

    proxy = scoremanagertools.proxies.StylesheetFileProxy()

    assert proxy.breadcrumb == 'stylesheet file proxy'
    assert not proxy.exists
    assert not proxy.file_lines
    assert proxy.generic_class_name == 'stylesheet'
    assert proxy.human_readable_name is None
    assert not proxy.is_versioned
    assert proxy.parent_directory_name is None
    assert proxy.path is None
    assert proxy.plural_generic_class_name == 'stylesheets'
    assert proxy.short_name is None
    assert proxy.short_name_without_extension is None
    assert proxy.svn_add_command is None
    assert proxy.temporary_asset_short_name == 'temporary_stylesheet.ly'


def test_StylesheetFileProxy_public_attributes_02():
    '''With path.
    '''

    short_name = 'clean_letter_14.ly'
    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    path = os.path.join(
        score_manager_configuration.SCORE_MANAGEMENT_TOOLS_DIRECTORY_PATH,
        'stylesheets', short_name)
    proxy = scoremanagertools.proxies.StylesheetFileProxy(path)

    assert proxy.breadcrumb == 'clean_letter_14.ly'
    assert proxy.exists
    assert proxy.file_lines
    assert proxy.generic_class_name == 'stylesheet'
    assert proxy.human_readable_name == short_name
    assert proxy.is_versioned
    assert proxy.parent_directory_name == proxy.configuration.stylesheets_directory_name
    assert proxy.path == path
    assert proxy.plural_generic_class_name == 'stylesheets'
    assert proxy.short_name == short_name
    assert proxy.short_name_without_extension == short_name[:-3]
    assert proxy.svn_add_command == 'svn add {}'.format(proxy.path)
    assert proxy.temporary_asset_short_name == 'temporary_stylesheet.ly'
