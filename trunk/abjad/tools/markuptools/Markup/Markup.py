from abjad.tools import abctools
from abjad.tools import schemetools
from abjad.tools import stringtools
from abjad.tools.marktools.DirectedMark.DirectedMark import DirectedMark


class Markup(DirectedMark):
    r'''Abjad model of LilyPond markup.

    Initialize from string::

        >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')

    ::

        >>> markup
        Markup((MarkupCommand('bold', ['This is markup text.']),))

    ::

        >>> f(markup)
        \markup { \bold { "This is markup text." } }

    Initialize any markup from existing markup::

        >>> markup_1 = markuptools.Markup('foo', direction=Up)
        >>> markup_2 = markuptools.Markup(markup_1, direction=Down)

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
        Markup((MarkupCommand('bold', ['This is markup text.']),))(c'4)

    ::

        >>> f(note)
        c'4 - \markup { \bold { "This is markup text." } }

    Set `direction` to ``Up``, ``Down``, ``'neutral'``, 
    ``'^'``, ``'_'``, ``'-'`` or None.

    Markup objects are immutable.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_contents', '_direction', '_format_slot', '_markup_name')

    _default_mandatory_input_arguments = (repr(r'\bold { "This is markup text." }'), )

    ### INITIALIZER ###

    def __init__(self, argument, direction=None, markup_name=None):
        from abjad.tools import lilypondparsertools
        from abjad.tools import markuptools
        if isinstance(argument, str):
            to_parse = r'\markup {{ {} }}'.format(argument)
            parsed = lilypondparsertools.LilyPondParser()(to_parse)
            if all([isinstance(x, str) for x in parsed.contents]):
                contents = (' '.join(parsed.contents),)
            else:
                contents = parsed.contents          
        elif isinstance(argument, markuptools.MarkupCommand):
            contents = (argument,)
        elif isinstance(argument, type(self)):
            contents = argument._contents
            direction = direction or argument._direction
            markup_name = markup_name or argument._markup_name
        elif isinstance(argument, (list, tuple)) and 0 < len(argument):
            contents = []
            for arg in argument:
                if isinstance(arg, (str, markuptools.MarkupCommand)):
                    contents.append(arg)
                else:
                    contents.append(str(arg))
            contents = tuple(contents)
        else:
            contents = (str(argument),)
        DirectedMark.__init__(self, direction=direction)
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
            (MarkupCommand('bold', ['This is markup text.']),)

        Return string
        '''
        return self._contents

    @property
    def indented_lilypond_format(self):
        r'''Read-only indented LilyPond format of markup::

            >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')
            >>> print markup.indented_lilypond_format
            \markup {
                \bold {
                    "This is markup text."
                    }
                }

        Return string.
        '''
        return '\n'.join(self._get_format_pieces(is_indented=True))

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

        direction = ''
        if self.direction is not None:
            direction = stringtools.arg_to_tridirectional_lilypond_symbol(self.direction)

        # a single string
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            if '"' in content:
                content = schemetools.format_scheme_value(content)
            if direction:
                return [r'{} \markup {{ {} }}'.format(direction, content)]
            return [r'\markup {{ {} }}'.format(content)]

        # multiple strings or markup commands
        if direction:
            pieces = [r'{} \markup {{'.format(direction)]
        else:
            pieces = [r'\markup {']
        for content in self.contents:
            if isinstance(content, str):
                content = schemetools.format_scheme_value(content)
                pieces.append('{}{}'.format(indent, content))
            else:
                pieces.extend(['{}{}'.format(indent, x) for x in
                    content._get_format_pieces(is_indented=is_indented)])
        pieces.append('{}}}'.format(indent))

        return pieces

    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        result = []
        indent = '\t'
        if not is_indented:
            indent = ''
        result.append('{}(('.format(self._tools_package_qualified_class_name))
        for i, content in enumerate(self.contents):
            comma = ','
            if 1 < len(self.contents) and i == len(self.contents) - 1:
                comma = ''
            if isinstance(content, abctools.AbjadObject):
                pieces = content._get_tools_package_qualified_repr_pieces()
                for piece in pieces[:-1]:
                    result.append('{}{}'.format(indent, piece))
                result.append('{}{}{}'.format(indent, pieces[-1], comma))
            else:
                result.append('{}{!r}{}'.format(indent, content, comma))
        strings = self._keyword_argument_name_value_strings
        if strings:
            result.append('{}),'.format(indent))
            for string in strings[:-1]:
                result.append('{}{},'.format(indent, string))
            result.append('{}{}'.format(indent, strings[-1]))
            result.append('{})'.format(indent))
        else:
            result.append('{}))'.format(indent))
        return result
