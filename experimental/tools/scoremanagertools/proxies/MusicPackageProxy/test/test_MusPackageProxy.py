import os
from experimental import *


def test_MusPackageProxy_01():

    music_proxy = scoremanagertools.proxies.MusicPackageProxy(
        'scoremanagertools.built_in_scores.example_score_1')

    assert music_proxy.filesystem_path == os.path.join(
        music_proxy.configuration.score_manager_tools_directory_path, 
        'built_in_scores', 'example_score_1', 'music')
    assert music_proxy.filesystem_basename == 'music'
    assert music_proxy.package_path == 'scoremanagertools.built_in_scores.example_score_1.music'
