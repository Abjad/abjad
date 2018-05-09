import abjad
import textwrap
import abjad.book


def test_1():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  shell::

        echo "foo"
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <literal_block language="console" xml:space="preserve">
                abjad$ echo "foo"
                foo
        ''')
    assert result == expected
