from abjad.tools.marktools._DirectedMark._DirectedMark import _DirectedMark
from abjad.tools.markuptools.MarkupCommand import MarkupCommand


class Markup(_DirectedMark):
    r'''Abjad model of LilyPond markup.

    Initialize from string::

        >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')

    ::

        >>> markup
        Markup(('\\bold { "This is markup text." }',))

    ::

        >>> f(markup)
        \markup { \bold { "This is markup text." } }

    Initialize any markup from existing markup::

        >>> markup_1 = markuptools.Markup('foo', direction='up')
        >>> markup_2 = markuptools.Markup(markup_1, direction='down')

    ::

        >>> f(markup_1)
        ^ \markup { foo }

    ::

        >>> f(markup_2) # doctest: +SKIP
        _ \markup { foo }

    Attach markup to score components like this::

        >>> note = Note("c'4")

    ::

        >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')

    ::

        >>> markup(note)
        Markup(('\\bold { "This is markup text." }',))(c'4)

    ::

        >>> f(note)
        c'4 - \markup { \bold { "This is markup text." } }

    Set `direction` to ``'up'``, ``'down'``, ``'neutral'``, 
    ``'^'``, ``'_'``, ``'-'`` or None.

    Markup objects are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_contents', '_direction', '_format_slot', '_markup_name')

    _default_mandatory_input_arguments = (repr(r'\bold { "This is markup text." }'), )

    ### INITIALIZER ###

    def __init__(self, argument, direction=None, markup_name=None):
        if isinstance(argument, (str, MarkupCommand)):
            contents = (argument,)
        elif isinstance(argument, Markup):
            contents = argument._contents
            direction = direction or argument._direction
            markup_name = markup_name or argument._markup_name
        elif isinstance(argument, (list, tuple)) and 0 < len(argument):
            contents = []
            for arg in argument:
                if isinstance(arg, (str, MarkupCommand)):
                    contents.append(arg)
                else:
                    contents.append(str(arg))
            contents = tuple(contents)
        else:
            contents = (str(argument),)
        _DirectedMark.__init__(self, direction=direction)
        self._contents = tuple(contents)
        self._format_slot = 'right'
        self._markup_name = markup_name

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            self._contents,
            direction=self._direction, 
            markup_name=self._markup_name,
            )

    __deepcopy__ = __copy__

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.lilypond_format == expr.lilypond_format:
                return True
        return False

    def __hash__(self):
        return hash((type(self).__name__, self.contents))

    def __ne__(self, expr):
        return not self == expr

    def __str__(self):
        return self.lilypond_format

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _format_pieces(self):
        return self._get_format_pieces(is_indented=False)

    @property
    def _mandatory_argument_values(self):
        return (
            self.contents,
            )

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Read-only tuple of contents of markup:

        ::

            >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')
            >>> markup.contents
            ('\\bold { "This is markup text." }',)

        Return string
        '''
        return self._contents

    @property
    def lilypond_format(self):
        r'''Read-only LilyPond format of markup::

            >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')
            >>> markup.lilypond_format
            '\\markup { \\bold { "This is markup text." } }'

        Return string.
        '''
        return ' '.join(self._get_format_pieces(is_indented=False))

    @property
    def markup_name(self):
        r'''Read-only name of markup::

            >>> markup = markuptools.Markup(
            ...     r'\bold { allegro ma non troppo }', markup_name='non troppo')

        ::

            >>> markup.markup_name
            'non troppo'

        Return string or none.
        '''
        return self._markup_name

    ### PRIVATE METHODS ###

    def _get_format_pieces(self, is_indented=True):
        indent = ''
        if is_indented:
            indent = '\t'

        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            if self.direction is not None:
                return [r'{} \markup {{ {} }}'.format(self.direction, self.contents[0])]
            return [r'\markup {{ {} }}'.format(self.contents[0])]

        if self.direction is not None:
            pieces = [r'{} \markup {{'.format(self.direction)]
        else:
            pieces = [r'\markup {']
        for content in self.contents:
            if isinstance(content, str):
                pieces.append('{}{}'.format(indent, content))
            else:
                pieces.extend(['{}{}'.format(indent, x) for x in
                    content._get_format_pieces(is_indented=is_indented)])
        pieces.append('{}}}'.format(indent))

        return pieces

