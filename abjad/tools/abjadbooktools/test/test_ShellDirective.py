# -*- coding: utf-8 -*-
import platform
import textwrap
import unittest
from abjad.tools import abjadbooktools
from abjad.tools import stringtools


@unittest.skipIf(platform.system() == 'Windows', 'No "echo" on Windows')
class ShellDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  shell::

            echo "foo"
        ''')
        document = self.handler.parse_rst(source)
        result = stringtools.normalize(document.pformat())
        expected = stringtools.normalize(
            r'''
            <document source="test">
                <literal_block language="console" xml:space="preserve">
                    abjad$ echo "foo"
                    foo
            ''')
        self.assertEqual(result, expected)
