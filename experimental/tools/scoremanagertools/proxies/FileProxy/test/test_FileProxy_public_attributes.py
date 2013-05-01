import os
from experimental import *


def test_FileProxy_public_attributes_01():
    '''Without path.
    '''

    file_proxy = scoremanagertools.proxies.FileProxy()

    assert not file_proxy.file_lines
    assert file_proxy.generic_class_name == 'file'
    assert file_proxy.space_delimited_lowercase_name is None
    assert not file_proxy.is_versioned
    assert file_proxy.parent_directory_path is None
    assert file_proxy.file_path is None
    assert file_proxy.plural_generic_class_name == 'files'
    assert file_proxy.name is None
    assert file_proxy.name_without_extension is None
    assert file_proxy.svn_add_command is None
    assert file_proxy.temporary_asset_name == 'temporary_file.txt'


def test_FileProxy_public_attributes_02():
    '''With path.
    '''

    file_name = 'clean_letter_14.ly'
    score_manager_configuration = scoremanagertools.core.ScoreManagerConfiguration()
    file_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', file_name)
    file_proxy = scoremanagertools.proxies.FileProxy(file_path)

    assert file_proxy.file_lines
    assert file_proxy.generic_class_name == 'file'
    assert file_proxy.space_delimited_lowercase_name == file_name
    assert file_proxy.is_versioned
    assert file_proxy.parent_directory_path == file_proxy.configuration.stylesheets_directory_path
    assert file_proxy.file_path == file_path
    assert file_proxy.plural_generic_class_name == 'files'
    assert file_proxy.name == file_name
    assert file_proxy.name_without_extension == file_name[:-3]
    assert file_proxy.svn_add_command == 'svn add {}'.format(file_proxy.file_path)
    assert file_proxy.temporary_asset_name == 'temporary_file.txt'
