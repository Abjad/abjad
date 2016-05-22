# -*- coding: utf-8 -*-
import os
import platform
import shutil
import unittest
from abjad.tools import abjadbooktools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython.',
    )
class TestLaTeXDocumentHandler(unittest.TestCase):

    test_directory = os.path.dirname(__file__)
    assets_directory = os.path.join(test_directory, 'assets')
    source_valid_path = os.path.join(test_directory, 'source_valid.tex')
    with open(source_valid_path, 'r') as file_pointer:
        source_valid_contents = file_pointer.read()
    target_valid_path = os.path.join(test_directory, 'target_valid.tex')

    expected_valid_path = os.path.join(test_directory, 'expected_valid.tex')
    with open(expected_valid_path, 'r') as file_pointer:
        expected_valid_contents = file_pointer.read()
    expected_asset_names = (
        'graphviz-31410f5aefd17473e91ebc219ddff36e.dot',
        'graphviz-31410f5aefd17473e91ebc219ddff36e.pdf',
        'lilypond-1b096a6d9cb9b88d4b5b3218adde56fb.ly',
        'lilypond-1b096a6d9cb9b88d4b5b3218adde56fb.pdf',
        'lilypond-1ed6ab0c1e7b7628704dd0a1a5e5fc3c.ly',
        'lilypond-1ed6ab0c1e7b7628704dd0a1a5e5fc3c.pdf',
        'lilypond-77c0ad74436edb553b402e5b0b8a169c.ly',
        'lilypond-77c0ad74436edb553b402e5b0b8a169c.pdf',
        'lilypond-8305d0b5b224439d7e29f93b7dd8e2a5.ly',
        'lilypond-8305d0b5b224439d7e29f93b7dd8e2a5.pdf',
        'lilypond-906b8a91ca49cb9688b4b0c3130a6af8.ly',
        'lilypond-906b8a91ca49cb9688b4b0c3130a6af8.pdf',
        )

    stylesheet_path = os.path.join(test_directory, 'stylesheet.ily')
    expected_styled_path = os.path.join(test_directory, 'expected_styled.tex')
    with open(expected_styled_path, 'r') as file_pointer:
        expected_styled_contents = file_pointer.read()
    styled_asset_names = (
        #'graphviz-12601707db5ddc467e3296e8c680ba43.dot',
        #'graphviz-12601707db5ddc467e3296e8c680ba43.pdf',
        'graphviz-31410f5aefd17473e91ebc219ddff36e.dot',
        'graphviz-31410f5aefd17473e91ebc219ddff36e.pdf',
        'lilypond-181e079044c9ede879fdab4c6210e307.ly',
        'lilypond-181e079044c9ede879fdab4c6210e307.pdf',
        'lilypond-596920d02e0ba6b487db5620c653dff0.ly',
        'lilypond-596920d02e0ba6b487db5620c653dff0.pdf',
        'lilypond-65094681fb26989d1bb5d8de316375ad.ly',
        'lilypond-65094681fb26989d1bb5d8de316375ad.pdf',
        'lilypond-e2e00802e4b3461b91fe02a3b7154dcf.ly',
        'lilypond-e2e00802e4b3461b91fe02a3b7154dcf.pdf',
        'lilypond-f3953b1da413b83e0a2f0291cbeece1e.ly',
        'lilypond-f3953b1da413b83e0a2f0291cbeece1e.pdf',
        )

    configuration_path = os.path.join(test_directory, 'configuration.cfg')
    expected_configured_path = os.path.join(
        test_directory, 'expected_configured.tex')
    with open(expected_configured_path, 'r') as file_pointer:
        expected_configured_contents = file_pointer.read()

    def setUp(self):
        if os.path.exists(self.assets_directory):
            shutil.rmtree(self.assets_directory)
        if os.path.exists(self.target_valid_path):
            os.remove(self.target_valid_path)

    def tearDown(self):
        if os.path.exists(self.assets_directory):
            shutil.rmtree(self.assets_directory)
        if os.path.exists(self.target_valid_path):
            os.remove(self.target_valid_path)
        with open(self.source_valid_path, 'w') as file_pointer:
            file_pointer.write(self.source_valid_contents)

    def test_clean(self):
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler()
        with open(self.source_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_valid_contents
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler(clean=True)
        with open(self.source_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.source_valid_contents

    def test_configured(self):
        configuration = abjadbooktools.AbjadBookScript()._read_config(
            self.configuration_path)
        assert not os.path.exists(self.target_valid_path)
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler(
            configuration=configuration,
            output_file_path=self.target_valid_path,
            )
        assert os.path.exists(self.target_valid_path)
        assert os.path.exists(self.assets_directory)
        with open(self.target_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_configured_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.expected_asset_names

    def test_double_source(self):
        assert not os.path.exists(self.target_valid_path)
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler(output_file_path=self.target_valid_path)
        assert os.path.exists(self.target_valid_path)
        assert os.path.exists(self.assets_directory)
        with open(self.target_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_valid_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.expected_asset_names

    def test_return_source(self):
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        target_valid_contents = document_handler(return_source=True)
        assert target_valid_contents == self.expected_valid_contents
        #assert not os.path.exists(self.assets_directory)

    def test_single_source(self):
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler()
        assert os.path.exists(self.source_valid_path)
        assert os.path.exists(self.assets_directory)
        with open(self.source_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_valid_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.expected_asset_names

    def test_single_source_rebuild(self):
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler()
        assert os.path.exists(self.source_valid_path)
        assert os.path.exists(self.assets_directory)
        with open(self.source_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_valid_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.expected_asset_names
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler()
        assert os.path.exists(self.source_valid_path)
        assert os.path.exists(self.assets_directory)
        with open(self.source_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_valid_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.expected_asset_names

    def test_skip_rendering(self):
        assert not os.path.exists(self.target_valid_path)
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler(
            output_file_path=self.target_valid_path,
            skip_rendering=True,
            )
        assert os.path.exists(self.target_valid_path)
        assert not os.path.exists(self.assets_directory)
        with open(self.target_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_valid_contents

    def test_stylesheet(self):
        assert not os.path.exists(self.target_valid_path)
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_valid_path)
        document_handler(
            output_file_path=self.target_valid_path,
            stylesheet=self.stylesheet_path,
            )
        assert os.path.exists(self.target_valid_path)
        assert os.path.exists(self.assets_directory)
        with open(self.target_valid_path, 'r') as file_pointer:
            target_valid_contents = file_pointer.read()
        assert target_valid_contents == self.expected_styled_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.styled_asset_names
