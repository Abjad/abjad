# -*- encoding: utf-8 -*-
from abjad.tools import abctools
from abjad.tools import schemetools
from abjad.tools import stringtools
from abjad.tools.marktools.Mark import Mark


class Markup(Mark):
    r'''Abjad model of LilyPond markup.

    Initialize from string:

    ::

        >>> markup = markuptools.Markup(r'\bold { "This is markup text." }')

    ::

        >>> markup
        Markup((MarkupCommand('bold', ['This is markup text.']),))

    ..  doctest::

        >>> print format(markup)
        \markup { \bold { "This is markup text." } }

    ::

        >>> show(markup) # doctest: +SKIP

    Initialize any markup from existing markup:

    ::

        >>> markup_1 = markuptools.Markup('foo', direction=Up)
        >>> markup_2 = markuptools.Markup(markup_1, direction=Down)

    ..  doctest::

        >>> print format(markup_1)
        ^ \markup { foo }

    ..  doctest::

        >>> print format(markup_2) # doctest: +SKIP
        _ \markup { foo }

    Attach markup to score components by calling them on the component:

    ::

        >>> note = Note("c'4")

    ::

        >>> markup = markuptools.Markup(
        ...     r'\italic { "This is also markup text." }', direction=Up)

    ::

        >>> attach(markup, note)

    ..  doctest::

        >>> print format(note)
        c'4 ^ \markup { \italic { "This is also markup text." } }

    ::

        >>> show(note) # doctest: +SKIP

    Set `direction` to ``Up``, ``Down``, ``'neutral'``,
    ``'^'``, ``'_'``, ``'-'`` or None.

    Markup objects are immutable.

    Returns markup instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents',
        '_direction',
        '_format_slot',
        '_markup_name',
        )

    _default_positional_input_arguments = (
        repr(r'\bold { "This is markup text." }'),
        )

    ### INITIALIZER ###

    def __init__(self, argument, direction=None, markup_name=None):
        from abjad.tools import lilypondparsertools
        from abjad.tools import markuptools
        if not argument:
            contents = None
        elif isinstance(argument, str):
            to_parse = r'\markup {{ {} }}'.format(argument)
            parsed = lilypondparsertools.LilyPondParser()(to_parse)
            if all(isinstance(x, str) for x in parsed.contents):
                contents = (' '.join(parsed.contents),)
            else:
                contents = tuple(parsed.contents)
        elif isinstance(argument, markuptools.MarkupCommand):
            contents = (argument,)
        elif isinstance(argument, type(self)):
            contents = tuple(argument._contents)
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
        Mark.__init__(self)
        self._contents = contents
        self._format_slot = 'right'
        self._markup_name = markup_name
        self.direction = direction

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            self._contents,
            direction=self._direction,
            markup_name=self._markup_name,
            )

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if format(self) == format(expr):
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats markup.

        Set `format_specification` to `''`, `'lilypond'` or `'storage'`.
        Interprets `''` equal to `'lilypond'`.

        Returns string.
        '''
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return self._tools_package_qualified_indented_repr
        return str(self)

    def __hash__(self):
        return hash((type(self).__name__, self.contents))

    def __ne__(self, expr):
        return not self == expr

    def __str__(self):
        return self._lilypond_format

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return '\n'.join(self._get_format_pieces())

    @property
    def _positional_argument_values(self):
        return (
            self.contents,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        r'''Tuple of contents of markup:

        ::

            >>> markup = \
            ...     markuptools.Markup(r'\bold { "This is markup text." }')
            >>> markup.contents
            (MarkupCommand('bold', ['This is markup text.']),)

        Returns string
        '''
        return self._contents

    @apply
    def direction():
        def fget(self):
            return self._direction
        def fset(self, arg):
            self._direction = \
                stringtools.arg_to_tridirectional_ordinal_constant(arg)
        return property(**locals())

    @property
    def markup_name(self):
        r'''Name of markup:

        ::

            >>> markup = markuptools.Markup(
            ...     r'\bold { allegro ma non troppo }',
            ...     markup_name='non troppo')

        ::

            >>> markup.markup_name
            'non troppo'

        Returns string or none.
        '''
        return self._markup_name

    ### PRIVATE METHODS ###

    def _get_format_pieces(self):
        indent = '\t'
        direction = ''
        if self.direction is not None:
            direction = stringtools.arg_to_tridirectional_lilypond_symbol(
                self.direction)
        # None
        if self.contents is None:
            return [r'\markup { }']
        # a single string
        if len(self.contents) == 1 and isinstance(self.contents[0], str):
            content = self.contents[0]
            if '"' in content:
                content = schemetools.Scheme.format_scheme_value(content)
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
                content = schemetools.Scheme.format_scheme_value(content)
                pieces.append('{}{}'.format(indent, content))
            else:
                pieces.extend(['{}{}'.format(indent, x) for x in
                    content._get_format_pieces()])
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
