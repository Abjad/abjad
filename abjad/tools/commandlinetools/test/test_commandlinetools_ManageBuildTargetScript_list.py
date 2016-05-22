# -*- coding: utf-8 -*-
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    def test_list(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--new', 'big-version']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'medium-version']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'small-version']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--list']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Available build targets:
            big-version
            medium-version
            small-version
        ''')
