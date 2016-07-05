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

    maxDiff = None

    test_directory = os.path.dirname(__file__)
    assets_directory = os.path.join(test_directory, 'assets')
    source_valid_path = os.path.join(test_directory, 'source_valid.tex')
    with open(source_valid_path, 'r') as file_pointer:
        source_valid_contents = file_pointer.read().rstrip()
    target_valid_path = os.path.join(test_directory, 'target_valid.tex')

    expected_valid_path = os.path.join(test_directory, 'expected_valid.tex')
    with open(expected_valid_path, 'r') as file_pointer:
        expected_valid_contents = file_pointer.read().rstrip()
    expected_asset_names = (
        'graphviz-31410f5aefd17473e91ebc219ddff36e.dot',
        'graphviz-31410f5aefd17473e91ebc219ddff36e.pdf',
        'lilypond-159af81bc32aca4b263146c9052b99ec.ly',
        'lilypond-159af81bc32aca4b263146c9052b99ec.pdf',
        'lilypond-71f63c1f11f143bb0f7a2f7ddbc77d75.ly',
        'lilypond-71f63c1f11f143bb0f7a2f7ddbc77d75.pdf',
        'lilypond-9a3d90e80bc733e46a43d1ee30b68fa9.ly',
        'lilypond-9a3d90e80bc733e46a43d1ee30b68fa9.pdf',
        'lilypond-9e8d4612a88db8a2f31e974c78fc915d.ly',
        'lilypond-9e8d4612a88db8a2f31e974c78fc915d.pdf',
        'lilypond-fe5d1d78512d19b7f51b96c2ce9180f9.ly',
        'lilypond-fe5d1d78512d19b7f51b96c2ce9180f9.pdf',
        )

    stylesheet_path = os.path.join(test_directory, 'stylesheet.ily')
    expected_styled_path = os.path.join(test_directory, 'expected_styled.tex')
    with open(expected_styled_path, 'r') as file_pointer:
        expected_styled_contents = file_pointer.read().rstrip()
    styled_asset_names = (
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
        expected_configured_contents = file_pointer.read().rstrip()

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
        assert str(target_valid_contents) == str(self.expected_valid_contents)
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

    @unittest.skipIf(
        platform.system() == 'Windows',
        'Windows path-handling woes.'
        )
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
