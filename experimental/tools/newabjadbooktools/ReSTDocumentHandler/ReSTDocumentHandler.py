from experimental.tools.newabjadbooktools.TextualDocumentHandler \
    import TextualDocumentHandler


class ReSTDocumentHandler(TextualDocumentHandler):
    """A document handler for ReST documents:

    ::

        >>> document = '''Let's print something:
        ...
        ... <abjad>
        ... print "hello, world!"
        ... </abjad>
        ...
        ... And let's show some music too:
        ...
        ... <abjad>
        ... show(Note("c'4"))
        ... </abjad>
        ...
        ... That's it!
        ... '''

    ::

        >>> document_handler = newabjadbooktools.ReSTDocumentHandler(document)
        >>> source_to_code_block_mapping = document_handler.extract_code_blocks()
        >>> document_handler.execute_code_blocks()
        >>> rebuilt_document = document_handler.rebuild_document()
        >>> for line in rebuilt_document:
        ...     print repr(line)
        ...
        "Let's print something:"
        ''
        '::'
        ''
        '\t>>> print "hello, world!"'
        '\thello, world!'
        ''
        "And let's show some music too:"
        ''
        '::'
        ''
        '\t>>> show(Note("c\'4"))'
        ''
        '.. image:: assets/lilypond-dbceae26d3d5a6f87ebaa36541fc88b7.png'
        ''
        "That's it!"

    Return document handler.
    """

    ### PUBLIC PROPERTIES ###

    @property
    def image_format(self):
        from experimental.tools import newabjadbooktools
        return newabjadbooktools.PNGImageFormat()
