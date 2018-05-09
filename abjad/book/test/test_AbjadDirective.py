import abjad
import textwrap
import abjad.book


def test_1():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  abjad::

        note = Note("c'4")
        if True:
            note.written_pitch = "ds,"
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_input_block>
                <literal_block xml:space="preserve">
                    note = Note("c'4")
                    if True:
                        note.written_pitch = "ds,"
        ''')
    assert result == expected


def test_2():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  abjad::
        :allow-exceptions:
        :hide:
        :no-resize:
        :no-trim:
        :strip-prompt:
        :with-thumbnail:

        note = Note("c'4")
        if True:
            note.written_pitch = "ds,"
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_input_block allow-exceptions="True" hide="True" no-resize="True" no-trim="True" strip-prompt="True" with-thumbnail="True">
                <literal_block xml:space="preserve">
                    note = Note("c'4")
                    if True:
                        note.written_pitch = "ds,"
        ''')
    assert result == expected


def test_3():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  abjad::
        :allow-exceptions:
        :hide:
        :pages: 1-3, 5, 7-7, 10-8,
        :strip-prompt:

        assert True is False
        ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_input_block allow-exceptions="True" hide="True" pages="(1, 2, 3, 5, 7, 10, 9, 8)" strip-prompt="True">
                <literal_block xml:space="preserve">
                    assert True is False
        ''')
    assert result == expected


def test_4():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  abjad::
        :stylesheet: rhythm-maker-docs.ily

        abjad.show(Note("c'4"))
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_input_block stylesheet="rhythm-maker-docs.ily">
                <literal_block xml:space="preserve">
                    abjad.show(Note("c'4"))
        ''')
    assert result == expected


def test_5():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  abjad::
        :no-stylesheet:
        :stylesheet: rhythm-maker-docs.ily

        abjad.show(Note("c'4"))
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_input_block no-stylesheet="True">
                <literal_block xml:space="preserve">
                    abjad.show(Note("c'4"))
        ''')
    assert result == expected


def test_6():
    handler = abjad.book.SphinxDocumentHandler
    source = textwrap.dedent('''
    ..  abjad::
        :text-width: 80
        :with-columns: 2

        abjad.show(Note("c'4"))
    ''')
    document = handler.parse_rst(source)
    result = abjad.String.normalize(document.pformat())
    expected = abjad.String.normalize(
        r'''
        <document source="test">
            <abjad_input_block text-width="80" with-columns="2">
                <literal_block xml:space="preserve">
                    abjad.show(Note("c'4"))
        ''')
    assert result == expected
