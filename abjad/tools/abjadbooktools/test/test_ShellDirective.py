# -*- encoding: utf-8 -*-
from abjad.tools import abjadbooktools
import textwrap
import unittest
from abjad.tools import systemtools


class ShellDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjadbooktools.SphinxDocumentHandler

    def test_1(self):
        source = textwrap.dedent('''
        ..  shell::

            echo "foo"
        ''')
        document = self.handler.parse_rst(source)
        result = systemtools.TestManager.clean_string(document.pformat())
        expected = systemtools.TestManager.clean_string(
            r'''
            <document source="test">
                <literal_block language="console" xml:space="preserve">
                    abjad$ echo "foo"
                    foo
            ''')
        self.assertEqual(result, expected)