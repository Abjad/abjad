import os
from experimental import *


def test_ScoreManagementObject_read_only_attributes_01():

    score_management_object = scoremanagementtools.core.ScoreManagementObject()

    path = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'boilerplate')
    assert score_management_object.configuration.boilerplate_directory_name == path

    assert isinstance(score_management_object.breadcrumb_stack, list)
    assert score_management_object.help_item_width == 5

    path = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'makers')
    assert score_management_object.makers_directory_name == path

    assert score_management_object.makers_package_importable_name == 'scoremanagementtools.makers'
    assert score_management_object.score_management_tools_package_importable_name == 'scoremanagementtools'

    path = os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH')
    assert score_management_object.score_management_tools_package_path_name == path

    assert isinstance(score_management_object.session, scoremanagementtools.core.Session)
    assert score_management_object.score_external_chunks_package_importable_name == 'sketches'

    path = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'core', 'ScoreManagementObject', 'ScoreManagementObject.py')
    assert score_management_object.source_file_name == path

    assert score_management_object._spaced_class_name == 'score management object'
    assert score_management_object.score_external_materials_package_importable_name == 'materials'


    path = os.path.join(os.environ.get('SCORE_MANAGEMENT_TOOLS_PATH'), 'stylesheets')
    assert score_management_object.stylesheets_directory_name == path

    assert score_management_object.stylesheets_package_importable_name == 'scoremanagementtools.stylesheets'
    assert isinstance(score_management_object.transcript, list)
    assert isinstance(score_management_object.transcript_signature, tuple)
    assert isinstance(score_management_object.ts, tuple)
