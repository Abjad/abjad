import os
from experimental import *


def test_Session_read_only_properties_01():
    '''Out of score.
    '''

    session = scoremanagementtools.core.Session()

    assert session.backtracking_stack == []
    assert session.breadcrumb_cache_stack == []
    assert session.breadcrumb_stack == []
    assert session.command_history == []
    assert session.command_history_string == ''
    assert isinstance(session.complete_transcript, scoremanagementtools.core.Transcript)

    assert session.current_chunks_package_importable_name == \
        os.path.basename(os.environ.get('SCORE_MANAGER_CHUNKS_DIRECTORY'))
    assert session.current_chunks_package_path_name == os.environ.get('SCORE_MANAGER_CHUNKS_DIRECTORY')

    assert session.current_materials_package_importable_name == \
        os.path.basename(os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY'))
    assert session.current_materials_package_path_name == os.environ.get('SCORE_MANAGER_MATERIALS_DIRECTORY')

    assert session.current_score_package_proxy is None
    assert session.current_score_path_name is None

    assert session.current_specifiers_package_importable_name == \
        os.path.basename(os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY'))
    assert session.current_specifiers_package_path_name == os.environ.get('SCORE_MANAGER_SPECIFIERS_DIRECTORY')

    assert session.explicit_command_history == []
    assert not session.is_complete
    assert session.is_displayable
    assert not session.is_in_score
    assert not session.is_navigating_to_sibling_score
    assert session.last_semantic_command is None
    assert session.menu_header == ''
    assert session.output_directory == os.environ.get('SCORE_MANAGER_TRANSCRIPTS_DIRECTORY')
    assert session.scores_to_show == 'active'
    assert not session.session_once_had_user_input
    assert session.testable_command_history_string == ''
    assert session.transcribe_next_command
    assert session.transcript == []
    assert not session.user_input_is_consumed


def test_Session_read_only_properties_02():
    '''In score.
    '''

    session = scoremanagementtools.core.Session()
    session.current_score_package_short_name = 'foo'

    assert session.current_chunks_package_importable_name == 'foo.mus.chunks'
    assert session.current_chunks_package_path_name == \
        os.path.join(os.environ.get('SCORES'), 'foo', 'mus', 'chunks')

    assert session.current_materials_package_importable_name == 'foo.mus.materials'
    assert session.current_materials_package_path_name == \
        os.path.join(os.environ.get('SCORES'), 'foo', 'mus', 'materials')

    assert isinstance(session.current_score_package_proxy, scoremanagementtools.proxies.ScorePackageProxy)
    assert session.current_score_path_name == os.path.join(os.environ.get('SCORES'), 'foo')

    assert session.current_specifiers_package_importable_name == 'foo.mus.specifiers'
    assert session.current_specifiers_package_path_name == \
        os.path.join(os.environ.get('SCORES'), 'foo', 'mus', 'specifiers')

    assert session.is_in_score
