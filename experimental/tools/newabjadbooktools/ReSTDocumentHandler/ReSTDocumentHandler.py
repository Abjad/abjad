from experimental.tools.newabjadbooktools.TextualDocumentHandler import \
    TextualDocumentHandler


class ReSTDocumentHandler(TextualDocumentHandler):
    """A document handler for ReST documents:

    ::

        >>> document = '''\
        ... Let's print something:
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

        >>> handler = newabjadbooktools.ReSTDocumentHandler(document)
        >>> code_blocks = handler.extract_code_blocks()
        >>> handler.execute_code_blocks()
        >>> rebuilt_document = handler.rebuild_document()
        >>> for line in rebuilt_document: # doctest: +SKIP
        ...     print repr(line)
        ...
        "Let's print something:"
        ''
        '::'
        ''
        '\t>>> print "hello, world!"'
        '\thello, world!'
        ''
        ''
        "And let's show some music too:"
        ''
        '::'
        ''
        '\t>>> show(Note("c\'4"))'
        ''
        '.. image:: lilypond-1dcefacf1c54cc60cef54588aab4b7fd.png'
        ''
        ''
        "That's it!"

    Return document handler.
    """

    pass
