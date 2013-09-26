# -*- encoding: utf-8 -*-
import os
from experimental import *


def test_FileProxy_public_attributes_01():
    r'''Without path.
    '''

    file_proxy = scoremanagertools.proxies.FileProxy()

    assert file_proxy._generic_class_name == 'file'
    assert file_proxy._space_delimited_lowercase_name is None
    assert not file_proxy.is_versioned()
    assert file_proxy.parent_directory_filesystem_path is None
    assert file_proxy.filesystem_path is None
    assert file_proxy._plural_generic_class_name == 'files'
    assert file_proxy.filesystem_basename is None
    assert file_proxy._repository_add_command is None
    assert file_proxy._temporary_asset_name == 'temporary_file.txt'


def test_FileProxy_public_attributes_02():
    r'''With path.
    '''

    file_name = 'clean-letter-14.ly'
    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', file_name)
    file_proxy = scoremanagertools.proxies.FileProxy(filesystem_path)

    assert file_proxy._generic_class_name == 'file'
    assert file_proxy._space_delimited_lowercase_name == file_name
    assert file_proxy.is_versioned()
    assert file_proxy.filesystem_path == filesystem_path
    assert file_proxy._plural_generic_class_name == 'files'
    assert file_proxy.filesystem_basename == file_name
    assert file_proxy._repository_add_command == 'svn add {}'.format(file_proxy.filesystem_path)
    assert file_proxy._temporary_asset_name == 'temporary_file.txt'
