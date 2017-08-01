# -*- coding: utf-8 -*-
import abjad
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    def test_list(self):
        self.create_score()
        script = abjad.commandlinetools.ManageBuildTargetScript()
        command = ['--new', 'big-version']
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'medium-version']
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--new', 'small-version']
        with abjad.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
        command = ['--list']
        with abjad.RedirectedStreams(stdout=self.string_io):
            with abjad.TemporaryDirectoryChange(str(self.score_path)):
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
