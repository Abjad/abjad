import os
from experimental import *


def test_MusicPackageProxy_01():

    music_proxy = scoremanagertools.proxies.MusicPackageProxy('example_score_1')

    assert music_proxy.directory_path == os.path.join(
        music_proxy.configuration.scores_directory_path, 'example_score_1', 'music')
    assert music_proxy.filesystem_basename == 'music'
    assert music_proxy.package_path == 'example_score_1.music'
