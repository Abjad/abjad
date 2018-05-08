import abjad
import textwrap
import unittest
import abjad.book


class ShellDirectiveTests(unittest.TestCase):

    def setUp(self):
        self.handler = abjad.book.SphinxDocumentHandler

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
