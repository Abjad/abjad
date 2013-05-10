import os
from experimental import *


def test_Session_read_only_properties_01():
    '''In score.
    '''

    session = scoremanagertools.core.Session()
    session.underscore_delimited_current_score_name = 'foo'

    assert session.current_segments_package_path == 'foo.music.segments'
    user_scores_directory_path = session.configuration.user_scores_directory_path
    assert session.current_segments_directory_path == \
        os.path.join(user_scores_directory_path, 'foo', 'music', 'segments')

    assert session.current_materials_package_path == 'foo.music.materials'
    assert session.current_materials_directory_path == \
        os.path.join(user_scores_directory_path, 'foo', 'music', 'materials')

    assert isinstance(session.current_score_package_proxy, scoremanagertools.proxies.ScorePackageProxy)

    assert session.current_specifiers_package_path == 'foo.music.specifiers'
    assert session.current_specifiers_directory_path == \
        os.path.join(user_scores_directory_path, 'foo', 'music', 'specifiers')

    assert session.is_in_score
