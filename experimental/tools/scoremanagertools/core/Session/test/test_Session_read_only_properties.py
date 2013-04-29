import os
from experimental import *


def test_Session_read_only_properties_01():
    '''Out of score.
    '''

    session = scoremanagertools.core.Session()

    assert session.backtracking_stack == []
    assert session.breadcrumb_cache_stack == []
    assert session._breadcrumb_stack == []
    assert session.command_history == []
    assert session.command_history_string == ''
    assert isinstance(session.complete_transcript, scoremanagertools.core.Transcript)

    assert session.current_segments_package_path == \
        os.path.basename(session.configuration.score_manager_sketches_directory_path)
    assert session.current_segments_directory_path == \
        session.configuration.score_manager_sketches_directory_path

    assert session.current_materials_package_path == \
        os.path.basename(session.configuration.score_manager_materials_directory_path)
    assert session.current_materials_directory_path == session.configuration.score_manager_materials_directory_path

    assert session.current_score_package_proxy is None
    assert session.current_score_path is None

    assert session.current_specifiers_package_path == \
        os.path.basename(session.configuration.score_manager_specifiers_directory_path)
    assert session.current_specifiers_directory_path == \
        session.configuration.score_manager_specifiers_directory_path
        
    assert session.explicit_command_history == []
    assert not session.is_complete
    assert session.is_displayable
    assert not session.is_in_score
    assert not session.is_navigating_to_sibling_score
    assert session.last_semantic_command is None
    assert session.menu_header == ''
    assert session.scores_to_show == 'active'
    assert not session.session_once_had_user_input
    assert session.testable_command_history_string == ''
    assert session.transcribe_next_command
    assert session.transcript == []
    assert not session.user_input_is_consumed


def test_Session_read_only_properties_02():
    '''In score.
    '''

    session = scoremanagertools.core.Session()
    session.current_score_package_name = 'foo'

    assert session.current_segments_package_path == 'foo.mus.chunks'
    scores_directory_path = session.configuration.scores_directory_path
    assert session.current_segments_directory_path == \
        os.path.join(scores_directory_path, 'foo', 'mus', 'chunks')

    assert session.current_materials_package_path == 'foo.mus.materials'
    assert session.current_materials_directory_path == \
        os.path.join(scores_directory_path, 'foo', 'mus', 'materials')

    assert isinstance(session.current_score_package_proxy, scoremanagertools.proxies.ScorePackageProxy)
    assert session.current_score_path == os.path.join(scores_directory_path, 'foo')

    assert session.current_specifiers_package_path == 'foo.mus.specifiers'
    assert session.current_specifiers_directory_path == \
        os.path.join(scores_directory_path, 'foo', 'mus', 'specifiers')

    assert session.is_in_score
