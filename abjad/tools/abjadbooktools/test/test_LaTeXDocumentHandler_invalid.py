# -*- coding: utf-8 -*-
import platform
import unittest
from abjad.tools import abjadbooktools


@unittest.skipIf(
    platform.python_implementation() != 'CPython',
    'Only for CPython',
    )
class TestLaTeXDocumentHandler_invalid(unittest.TestCase):

    maxDiff = None

    def test_invalid_source_1(self):
        input_file_contents = [
            '<abjad>',
            '<abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_2(self):
        input_file_contents = [
            '<abjad>',
            '%%% ABJADBOOK START %%%',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_3(self):
        input_file_contents = [
            '<abjad>',
            '%%% ABJADBOOK END %%%',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_4(self):
        input_file_contents = [
            '%%% ABJADBOOK START %%%',
            '%%% ABJADBOOK START %%%',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_5(self):
        input_file_contents = [
            '%%% ABJADBOOK START %%%',
            '<abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_6(self):
        input_file_contents = [
            '%%% ABJADBOOK START %%%',
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_7(self):
        input_file_contents = [
            ''
            '</abjad>',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )

    def test_invalid_source_8(self):
        input_file_contents = [
            ''
            '%%% ABJADBOOK END %%%',
            ]
        document_handler = abjadbooktools.LaTeXDocumentHandler(
            input_file_contents=input_file_contents,
            )
        self.assertRaises(
            ValueError,
            document_handler.__call__,
            )
