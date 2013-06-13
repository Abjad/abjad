from experimental.tools.newabjadbooktools.TextualDocumentHandler import TextualDocumentHandler


class HTMLDocumentHandler(TextualDocumentHandler):
    r"""A document handler for HTML documents:

    ::

        >>> document = '''<html>
        ... <head>
        ... </head>
        ... <body>
        ... Let's print something:
        ...
        ... <abjad>
        ... print "hello, world!"
        ... </abjad>
        ...
        ... This is just a simple Python string:
        ...
        ... <abjad>
        ... just_a_string = \'\'\'
        ... show(Nothing!)
        ... \'\'\'
        ... </abjad>
        ...
        ... And let's show some music too:
        ...
        ... <abjad>
        ... show(Note("c'4"))
        ... </abjad>
        ...
        ... That's it!
        ... </body>
        ... </html>
        ... '''

    ::

        >>> handler = newabjadbooktools.HTMLDocumentHandler(document)
        >>> code_blocks = handler.extract_code_blocks()
        >>> handler.execute_code_blocks()
        >>> rebuilt_document = handler.rebuild_document()
        >>> for line in rebuilt_document:
        ...     print repr(line)
        ...
        '<html>'
        '<head>'
        '</head>'
        '<body>'
        "Let's print something:"
        ''
        '<pre class="abjad">'
        '>>> print "hello, world!"'
        'hello, world!'
        '</pre>'
        ''
        'This is just a simple Python string:'
        ''
        '<pre class="abjad">'
        ">>> just_a_string = '''"
        '... show(Nothing!)'
        "... '''"
        '</pre>'
        '' 
        "And let's show some music too:"
        ''
        '<pre class="abjad">'
        '>>> show(Note("c\'4"))'
        '</pre>'
        ''
        '<img alt="" src="assets/lilypond-dbceae26d3d5a6f87ebaa36541fc88b7.png"/>'
        ''
        "That's it!"
        '</body>'
        '</html>'

    Return document handler.
    """

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def image_format(self):
        from experimental.tools import newabjadbooktools
        return newabjadbooktools.PNGImageFormat()
