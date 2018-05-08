import pathlib
import re
import shutil
import sys
import unittest


class ScorePackageScriptTestCase(unittest.TestCase):
    r'''A base test class for score-package scripts.
    '''

    ansi_escape = re.compile(r'\x1b[^m]*m')

    test_directory_path = pathlib.Path(__file__).parent
    score_path = test_directory_path.joinpath('test_score')
    build_path = score_path.joinpath('test_score', 'builds')
    distribution_path = score_path.joinpath('test_score', 'distribution')
    materials_path = score_path.joinpath('test_score', 'materials')
    segments_path = score_path.joinpath('test_score', 'segments')
    tools_path = score_path.joinpath('test_score', 'tools')

    # ### TEST LIFECYCLE ### #

    def setUp(self):
        if self.score_path.exists():
            shutil.rmtree(self.score_path)
        self.directory_items = set(self.test_directory_path.iterdir())
        sys.path.insert(0, str(self.score_path))

    def tearDown(self):
        for path in sorted(self.test_directory_path.iterdir()):
            if path in self.directory_items:
                continue
            if path.is_file():
                path.unlink()
            else:
                shutil.rmtree(path)
        sys.path.remove(str(self.score_path))
        for path, module in tuple(sys.modules.items()):
            if not path or not module:
                continue
            if path.startswith('test_score'):
                del(sys.modules[path])
