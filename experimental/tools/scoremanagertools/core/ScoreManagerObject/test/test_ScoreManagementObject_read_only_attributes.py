import os
from experimental import *


def test_ScoreManagementObject_read_only_attributes_01():

    score_manager_object = scoremanagertools.core.ScoreManagerObject()

    directory_path = os.path.join(
        score_manager_object.configuration.score_manager_tools_directory_path,
        'boilerplate')
    assert score_manager_object.configuration.boilerplate_directory_path == directory_path

    assert isinstance(score_manager_object.breadcrumb_stack, list)
    assert score_manager_object.help_item_width == 5

    directory_path = os.path.join(
        score_manager_object.configuration.score_manager_tools_directory_path,
        'makers')
    assert score_manager_object.configuration.makers_directory_path == directory_path

    assert score_manager_object.configuration.makers_package_path == 'scoremanagertools.makers'
    assert score_manager_object.configuration.score_manager_tools_package_path == \
        'scoremanagertools'

    assert isinstance(score_manager_object.session, scoremanagertools.core.Session)
    assert score_manager_object.configuration.score_external_chunks_package_path == 'sketches'

    file_path = os.path.join(
        score_manager_object.configuration.score_manager_tools_directory_path,
        'core', 'ScoreManagerObject', 'ScoreManagerObject.py')
    assert score_manager_object.source_file_name == file_path

    assert score_manager_object._spaced_class_name == 'score manager object'
    assert score_manager_object.configuration.score_external_materials_package_path == 'materials'


    directory_path = os.path.join(
        score_manager_object.configuration.score_manager_tools_directory_path,
        'stylesheets')
    assert score_manager_object.configuration.stylesheets_directory_path == directory_path

    assert score_manager_object.configuration.stylesheets_package_path == \
        'scoremanagertools.stylesheets'
    assert isinstance(score_manager_object.transcript, list)
    assert isinstance(score_manager_object.transcript_signature, tuple)
    assert isinstance(score_manager_object.ts, tuple)
