# -*- encoding: utf-8 -*-
import os
from experimental import *
import py.test


def test_FileManager_public_attributes_01():
    r'''Without path.
    '''

    file_manager = scoremanagertools.managers.FileManager()

    assert file_manager._generic_class_name == 'file'
    assert file_manager._space_delimited_lowercase_name is None
    assert not file_manager._is_versioned()
    assert file_manager.filesystem_path is None
    assert file_manager._plural_generic_class_name == 'files'
    assert file_manager._repository_add_command is None
    assert file_manager._temporary_asset_name == 'temporary_file.txt'


@py.test.skip('FIXME: Broken by git migration.')
def test_FileManager_public_attributes_02():
    r'''With path.
    '''

    file_name = 'clean-letter-14.ly'
    score_manager_configuration = scoremanagertools.scoremanager.ScoreManagerConfiguration()
    filesystem_path = os.path.join(
        score_manager_configuration.score_manager_tools_directory_path,
        'stylesheets', file_name)
    file_manager = scoremanagertools.managers.FileManager(filesystem_path)

    assert file_manager._generic_class_name == 'file'
    assert file_manager._space_delimited_lowercase_name == file_name
    assert file_manager._is_versioned()
    assert file_manager.filesystem_path == filesystem_path
    assert file_manager._plural_generic_class_name == 'files'
    assert file_manager._repository_add_command == 'svn add {}'.format(file_manager.filesystem_path)
    assert file_manager._temporary_asset_name == 'temporary_file.txt'
