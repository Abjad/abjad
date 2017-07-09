# -*- coding: utf-8 -*-
import abjad
import platform
import textwrap
import unittest


@unittest.skipIf(platform.system() == 'Windows', 'No "echo" on Windows')
class ShellDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjad.abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  shell::

            echo "foo"
        ''')
        document = self.handler.parse_rst(source)
        result = abjad.String.normalize(document.pformat())
        expected = abjad.String.normalize(
            r'''
            <document source="test">
                <literal_block language="console" xml:space="preserve">
                    abjad$ echo "foo"
                    foo
            ''')
        self.assertEqual(result, expected)
