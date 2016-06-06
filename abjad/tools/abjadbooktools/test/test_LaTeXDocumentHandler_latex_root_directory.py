# -*- coding: utf-8 -*-
import os
import platform
import shutil
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython.',
    )
class TestLaTeXDocumentHandler(unittest.TestCase):

    maxDiff = None

    test_directory = os.path.dirname(__file__)
    assets_directory = os.path.join(test_directory, 'assets')
    source_path = os.path.join(
        test_directory,
        'chapters',
        'chapter-1',
        'source.tex',
        )
    with open(source_path, 'r') as file_pointer:
        source_contents = file_pointer.read()
    target_path = os.path.join(
        test_directory,
        'chapters',
        'chapter-1',
        'target.tex',
        )
    expected_path = os.path.join(
        test_directory,
        'chapters',
        'chapter-1',
        'expected.tex',
        )
    with open(expected_path, 'r') as file_pointer:
        expected_contents = file_pointer.read()
    expected_asset_names = (
        'lilypond-fe5d1d78512d19b7f51b96c2ce9180f9.ly',
        'lilypond-fe5d1d78512d19b7f51b96c2ce9180f9.pdf',
        )

    def setUp(self):
        if os.path.exists(self.assets_directory):
            shutil.rmtree(self.assets_directory)
        if os.path.exists(self.target_path):
            os.remove(self.target_path)

    def tearDown(self):
        if os.path.exists(self.assets_directory):
            shutil.rmtree(self.assets_directory)
        if os.path.exists(self.target_path):
            os.remove(self.target_path)
        with open(self.source_path, 'w') as file_pointer:
            file_pointer.write(self.source_contents)

    def test_latex_root_directory_1(self):
        input_file_contents = [
            '\\begin{comment}',
            '<abjad>',
            'note = Note(0, (1, 4))',
            'show(note)',
            '</abjad>',
            '\\end{comment}',
            ]
        assets_directory = 'ExamplePaper/assets'
        input_file_path = 'ExamplePaper/chapters/chapter-1/section-2.tex'
        latex_root_directory = 'ExamplePaper'
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            assets_directory=assets_directory,
            input_file_contents=input_file_contents,
            input_file_path=input_file_path,
            latex_root_directory=latex_root_directory,
            )
        rebuilt_source = document_handler(return_source=True)
        assert rebuilt_source == stringtools.normalize(
            '''
            \\begin{comment}
            <abjad>
            note = Note(0, (1, 4))
            show(note)
            </abjad>
            \\end{comment}

            %%% ABJADBOOK START %%%
            \\begin{lstlisting}
            >>> note = Note(0, (1, 4))
            >>> show(note)
            \\end{lstlisting}
            \\noindent\\includegraphics{assets/lilypond-fe5d1d78512d19b7f51b96c2ce9180f9.pdf}
            %%% ABJADBOOK END %%%
            ''',
            )

    def test_latex_root_directory_2(self):
        assert not os.path.exists(self.target_path)
        assert not os.path.exists(self.assets_directory)
        document_handler = abjadbooktools.LaTeXDocumentHandler.from_path(
            input_file_path=self.source_path,
            assets_directory=self.assets_directory,
            latex_root_directory=self.test_directory,
            )
        document_handler(output_file_path=self.target_path)
        assert os.path.exists(self.target_path)
        assert os.path.exists(self.assets_directory)
        with open(self.target_path, 'r') as file_pointer:
            target_contents = file_pointer.read()
        assert target_contents == self.expected_contents
        assert tuple(sorted(os.listdir(self.assets_directory))) == \
            self.expected_asset_names
