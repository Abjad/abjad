import abjad
import abjad.book
import textwrap


def test_1():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  import:: abjad.tools.topleveltools.attach
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_import_block path="abjad.tools.topleveltools.attach">
        ''')
    assert result == expected


def test_2():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  import:: abjad.tools.topleveltools.attach
        :hide:
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_import_block hide="True" path="abjad.tools.topleveltools.attach">
        ''')
    assert result == expected
