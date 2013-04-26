import os
from experimental import *


def test_ScoreManagementObject_read_only_attributes_01():

    score_manager_object = scoremanagertools.core.ScoreManagerObject()

    path = os.path.join(
        score_manager_object.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
        'boilerplate')
    assert score_manager_object.configuration.BOILERPLATE_DIRECTORY_PATH == path

    assert isinstance(score_manager_object.breadcrumb_stack, list)
    assert score_manager_object.help_item_width == 5

    path = os.path.join(
        score_manager_object.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
        'makers')
    assert score_manager_object.configuration.makers_directory_path == path

    assert score_manager_object.configuration.makers_package_importable_name == 'scoremanagertools.makers'
    assert score_manager_object.configuration.score_manager_tools_package_importable_name == \
        'scoremanagertools'

    assert isinstance(score_manager_object.session, scoremanagertools.core.Session)
    assert score_manager_object.configuration.score_external_chunks_package_importable_name == 'sketches'

    path = os.path.join(
        score_manager_object.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
        'core', 'ScoreManagerObject', 'ScoreManagerObject.py')
    assert score_manager_object.source_file_name == path

    assert score_manager_object._spaced_class_name == 'score manager object'
    assert score_manager_object.configuration.score_external_materials_package_importable_name == 'materials'


    path = os.path.join(
        score_manager_object.configuration.SCORE_MANAGER_TOOLS_DIRECTORY_PATH,
        'stylesheets')
    assert score_manager_object.configuration.stylesheets_directory_path == path

    assert score_manager_object.configuration.stylesheets_package_importable_name == \
        'scoremanagertools.stylesheets'
    assert isinstance(score_manager_object.transcript, list)
    assert isinstance(score_manager_object.transcript_signature, tuple)
    assert isinstance(score_manager_object.ts, tuple)
